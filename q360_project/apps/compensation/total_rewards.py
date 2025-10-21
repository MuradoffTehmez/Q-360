"""
Total Rewards Statement Generator.
Creates comprehensive compensation and benefits statements for employees.
"""
from decimal import Decimal
from datetime import datetime, date
from django.db.models import Sum, Avg
from .models import (
    SalaryInformation, Bonus, Allowance, Deduction,
    EquityGrant, MarketBenchmark
)


class TotalRewardsCalculator:
    """
    Calculates total rewards including salary, bonuses, benefits, and equity.
    """

    def __init__(self, user, fiscal_year=None):
        """
        Initialize calculator for a user.

        Args:
            user: User instance
            fiscal_year: Year for calculation (defaults to current year)
        """
        self.user = user
        self.fiscal_year = fiscal_year or datetime.now().year

    def calculate_base_compensation(self):
        """Calculate base salary compensation."""
        try:
            salary_info = SalaryInformation.objects.filter(
                user=self.user,
                is_active=True
            ).latest('effective_date')

            # Annualize based on payment frequency
            if salary_info.payment_frequency == 'monthly':
                annual_base = salary_info.base_salary * 12
            elif salary_info.payment_frequency == 'biweekly':
                annual_base = salary_info.base_salary * 26
            elif salary_info.payment_frequency == 'weekly':
                annual_base = salary_info.base_salary * 52
            else:
                annual_base = salary_info.base_salary

            return {
                'base_salary': salary_info.base_salary,
                'payment_frequency': salary_info.payment_frequency,
                'annual_base': annual_base,
                'currency': salary_info.currency
            }
        except SalaryInformation.DoesNotExist:
            return {
                'base_salary': Decimal('0'),
                'payment_frequency': 'monthly',
                'annual_base': Decimal('0'),
                'currency': 'AZN'
            }

    def calculate_bonuses(self):
        """Calculate total bonuses for fiscal year."""
        bonuses = Bonus.objects.filter(
            user=self.user,
            fiscal_year=self.fiscal_year,
            status__in=['approved', 'paid']
        )

        total = bonuses.aggregate(total=Sum('amount'))['total'] or Decimal('0')

        bonus_breakdown = []
        for bonus in bonuses:
            bonus_breakdown.append({
                'type': bonus.get_bonus_type_display(),
                'amount': bonus.amount,
                'status': bonus.get_status_display(),
                'description': bonus.description
            })

        return {
            'total_bonuses': total,
            'count': bonuses.count(),
            'breakdown': bonus_breakdown
        }

    def calculate_allowances(self):
        """Calculate total allowances."""
        active_allowances = Allowance.objects.filter(
            user=self.user,
            is_active=True,
            start_date__lte=date.today()
        ).filter(
            models.Q(end_date__isnull=True) | models.Q(end_date__gte=date.today())
        )

        total_annual = Decimal('0')
        allowance_breakdown = []

        for allowance in active_allowances:
            # Annualize based on frequency
            if allowance.payment_frequency == 'monthly':
                annual_value = allowance.amount * 12
            elif allowance.payment_frequency == 'quarterly':
                annual_value = allowance.amount * 4
            elif allowance.payment_frequency == 'annual':
                annual_value = allowance.amount
            else:  # one_time
                annual_value = allowance.amount

            total_annual += annual_value

            allowance_breakdown.append({
                'type': allowance.get_allowance_type_display(),
                'amount': allowance.amount,
                'frequency': allowance.get_payment_frequency_display(),
                'annual_value': annual_value,
                'taxable': allowance.is_taxable
            })

        return {
            'total_annual_allowances': total_annual,
            'count': active_allowances.count(),
            'breakdown': allowance_breakdown
        }

    def calculate_deductions(self):
        """Calculate total deductions."""
        active_deductions = Deduction.objects.filter(
            user=self.user,
            is_active=True,
            start_date__lte=date.today()
        ).filter(
            models.Q(end_date__isnull=True) | models.Q(end_date__gte=date.today())
        )

        total_annual = Decimal('0')
        deduction_breakdown = []

        for deduction in active_deductions:
            # For percentage-based, need to calculate based on salary
            if deduction.calculation_method == 'percentage':
                base_comp = self.calculate_base_compensation()
                annual_value = (base_comp['annual_base'] * deduction.amount) / 100
            else:
                # Fixed amount - assume monthly
                annual_value = deduction.amount * 12

            total_annual += annual_value

            deduction_breakdown.append({
                'type': deduction.get_deduction_type_display(),
                'amount': deduction.amount,
                'method': deduction.get_calculation_method_display(),
                'annual_value': annual_value
            })

        return {
            'total_annual_deductions': total_annual,
            'count': active_deductions.count(),
            'breakdown': deduction_breakdown
        }

    def calculate_equity_value(self):
        """Calculate current value of equity grants."""
        equity_grants = EquityGrant.objects.filter(
            user=self.user,
            status__in=['vesting', 'vested']
        )

        total_vested_value = Decimal('0')
        total_unvested_value = Decimal('0')
        equity_breakdown = []

        for grant in equity_grants:
            vested_value = grant.calculate_current_value()
            total_vested_value += vested_value

            # Calculate unvested value
            if grant.current_share_value:
                unvested_value = Decimal(grant.unvested_shares) * grant.current_share_value
                total_unvested_value += unvested_value

            equity_breakdown.append({
                'type': grant.get_equity_type_display(),
                'total_shares': grant.number_of_shares,
                'vested_shares': grant.vested_shares,
                'unvested_shares': grant.unvested_shares,
                'vested_value': vested_value,
                'grant_date': grant.grant_date,
                'vesting_progress': (grant.vested_shares / grant.number_of_shares) * 100 if grant.number_of_shares > 0 else 0
            })

        return {
            'total_vested_value': total_vested_value,
            'total_unvested_value': total_unvested_value,
            'total_equity_value': total_vested_value + total_unvested_value,
            'count': equity_grants.count(),
            'breakdown': equity_breakdown
        }

    def calculate_total_rewards(self):
        """Calculate complete total rewards package."""
        base_comp = self.calculate_base_compensation()
        bonuses = self.calculate_bonuses()
        allowances = self.calculate_allowances()
        deductions = self.calculate_deductions()
        equity = self.calculate_equity_value()

        # Calculate total cash compensation
        total_cash = (
            base_comp['annual_base'] +
            bonuses['total_bonuses'] +
            allowances['total_annual_allowances'] -
            deductions['total_annual_deductions']
        )

        # Total compensation including equity
        total_compensation = total_cash + equity['total_equity_value']

        return {
            'fiscal_year': self.fiscal_year,
            'base_compensation': base_comp,
            'bonuses': bonuses,
            'allowances': allowances,
            'deductions': deductions,
            'equity': equity,
            'total_cash_compensation': total_cash,
            'total_compensation': total_compensation,
            'currency': base_comp['currency']
        }


class TotalRewardsStatementGenerator:
    """
    Generates formatted Total Rewards Statements for employees.
    """

    def __init__(self, user, fiscal_year=None):
        """
        Initialize generator.

        Args:
            user: User instance
            fiscal_year: Year for statement
        """
        self.user = user
        self.fiscal_year = fiscal_year or datetime.now().year
        self.calculator = TotalRewardsCalculator(user, fiscal_year)

    def generate_statement(self, include_market_comparison=True):
        """
        Generate complete total rewards statement.

        Args:
            include_market_comparison: Whether to include market benchmarking data

        Returns:
            dict: Complete statement data
        """
        rewards = self.calculator.calculate_total_rewards()

        statement = {
            'employee': {
                'name': self.user.get_full_name(),
                'email': self.user.email,
                'employee_id': self.user.username,
                'department': self.user.department.name if hasattr(self.user, 'department') and self.user.department else 'N/A',
                'position': getattr(self.user, 'position_title', 'N/A')
            },
            'statement_date': datetime.now().date(),
            'fiscal_year': self.fiscal_year,
            'rewards': rewards,
            'summary': self._generate_summary(rewards)
        }

        if include_market_comparison:
            statement['market_comparison'] = self._get_market_comparison(rewards)

        return statement

    def _generate_summary(self, rewards):
        """Generate executive summary of compensation."""
        return {
            'total_value': rewards['total_compensation'],
            'cash_compensation': rewards['total_cash_compensation'],
            'equity_value': rewards['equity']['total_equity_value'],
            'components_count': (
                1 +  # Base salary
                rewards['bonuses']['count'] +
                rewards['allowances']['count'] +
                rewards['equity']['count']
            ),
            'highlights': self._generate_highlights(rewards)
        }

    def _generate_highlights(self, rewards):
        """Generate key highlights from compensation package."""
        highlights = []

        # Base salary
        base = rewards['base_compensation']['annual_base']
        highlights.append(f"Base Maaş: {base:,.2f} {rewards['currency']}")

        # Bonuses
        if rewards['bonuses']['total_bonuses'] > 0:
            highlights.append(f"Bonuslar: {rewards['bonuses']['total_bonuses']:,.2f} {rewards['currency']}")

        # Allowances
        if rewards['allowances']['total_annual_allowances'] > 0:
            highlights.append(f"Müavinətlər: {rewards['allowances']['total_annual_allowances']:,.2f} {rewards['currency']}")

        # Equity
        if rewards['equity']['total_equity_value'] > 0:
            highlights.append(f"Səhm Dəyəri: {rewards['equity']['total_equity_value']:,.2f} USD")

        return highlights

    def _get_market_comparison(self, rewards):
        """Get market comparison data if available."""
        try:
            # Find relevant benchmark
            position = getattr(self.user, 'position_title', None)
            if not position:
                return None

            benchmark = MarketBenchmark.objects.filter(
                position_title__icontains=position,
                is_active=True
            ).order_by('-data_date').first()

            if not benchmark:
                return None

            # Compare current total cash to market
            total_cash = rewards['total_cash_compensation']
            comparison = benchmark.compare_to_salary(total_cash)

            return {
                'benchmark': {
                    'position': benchmark.position_title,
                    'median_salary': benchmark.median_salary,
                    'min_salary': benchmark.min_salary,
                    'max_salary': benchmark.max_salary,
                    'data_date': benchmark.data_date,
                    'source': benchmark.get_data_source_display()
                },
                'comparison': comparison,
                'message': self._get_comparison_message(comparison)
            }

        except Exception as e:
            return None

    def _get_comparison_message(self, comparison):
        """Generate human-readable market comparison message."""
        if comparison['is_competitive']:
            return f"Maaşınız bazar median-ına uyğundur (Persentil: {comparison['percentile']:.1f})"
        elif comparison['position'] == 'below_min':
            return "Maaşınız bazar minimum-undan aşağıdadır"
        elif comparison['position'] == 'above_max':
            return "Maaşınız bazar maksimum-undan yuxarıdadır"
        else:
            diff = abs(comparison['difference_percent'])
            if comparison['difference_percent'] < 0:
                return f"Maaşınız bazar median-ından {diff:.1f}% aşağıdadır"
            else:
                return f"Maaşınız bazar median-ından {diff:.1f}% yuxarıdadır"

    def generate_html_statement(self):
        """Generate HTML formatted statement."""
        statement = self.generate_statement()

        # In production, use proper template
        html = f"""
        <html>
        <head>
            <title>Total Rewards Statement - {self.user.get_full_name()}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background: #2c3e50; color: white; padding: 20px; }}
                .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; }}
                .amount {{ font-size: 24px; font-weight: bold; color: #27ae60; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Total Rewards Statement</h1>
                <p>{statement['fiscal_year']} Maliyyə İli</p>
                <p>{statement['employee']['name']} - {statement['employee']['position']}</p>
            </div>

            <div class="section">
                <h2>Ümumi Mükafatlandırma</h2>
                <div class="amount">{statement['summary']['total_value']:,.2f} {statement['rewards']['currency']}</div>
            </div>

            <div class="section">
                <h2>Kompensasiya Komponenetləri</h2>
                <table>
                    <tr>
                        <th>Komponent</th>
                        <th>İllik Dəyər</th>
                    </tr>
                    <tr>
                        <td>Əsas Maaş</td>
                        <td>{statement['rewards']['base_compensation']['annual_base']:,.2f}</td>
                    </tr>
                    <tr>
                        <td>Bonuslar</td>
                        <td>{statement['rewards']['bonuses']['total_bonuses']:,.2f}</td>
                    </tr>
                    <tr>
                        <td>Müavinətlər</td>
                        <td>{statement['rewards']['allowances']['total_annual_allowances']:,.2f}</td>
                    </tr>
                    <tr>
                        <td>Səhm Dəyəri</td>
                        <td>{statement['rewards']['equity']['total_equity_value']:,.2f}</td>
                    </tr>
                </table>
            </div>
        </body>
        </html>
        """

        return html

    def generate_pdf_statement(self):
        """Generate PDF statement (requires reportlab or similar)."""
        # Placeholder for PDF generation
        # In production, use reportlab or weasyprint
        html = self.generate_html_statement()

        # Convert HTML to PDF
        # from weasyprint import HTML
        # pdf = HTML(string=html).write_pdf()

        return None  # Placeholder


# Helper function for easy access
def generate_total_rewards_statement(user, fiscal_year=None, format='dict'):
    """
    Generate total rewards statement for a user.

    Args:
        user: User instance
        fiscal_year: Fiscal year for statement
        format: Output format ('dict', 'html', 'pdf')

    Returns:
        Statement in requested format
    """
    generator = TotalRewardsStatementGenerator(user, fiscal_year)

    if format == 'html':
        return generator.generate_html_statement()
    elif format == 'pdf':
        return generator.generate_pdf_statement()
    else:
        return generator.generate_statement()
