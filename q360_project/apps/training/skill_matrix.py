"""
Skill Matrix and Gap Analysis Module.
Tracks employee skills, competencies, and identifies skill gaps.
"""
from django.db.models import Avg, Count, Q
from decimal import Decimal
from typing import Dict, List
from apps.competencies.models import Competency, UserCompetency


class SkillMatrix:
    """
    Creates and manages skill matrices for teams, departments, or individuals.
    """

    def __init__(self, users=None, department=None, competencies=None):
        """
        Initialize skill matrix.

        Args:
            users: QuerySet or list of User instances
            department: Department instance
            competencies: QuerySet or list of Competency instances
        """
        self.users = users
        self.department = department
        self.competencies = competencies

    def generate_matrix(self):
        """
        Generate complete skill matrix.

        Returns:
            dict: Matrix data with users, competencies, and proficiency levels
        """
        # Get users
        if self.users is None and self.department:
            from apps.accounts.models import User
            users = User.objects.filter(department=self.department, is_active=True)
        else:
            users = self.users

        if not users:
            return {'error': 'No users specified'}

        # Get competencies
        if self.competencies is None:
            competencies = Competency.objects.filter(is_active=True)
        else:
            competencies = self.competencies

        # Build matrix
        matrix = {
            'metadata': {
                'user_count': users.count() if hasattr(users, 'count') else len(users),
                'competency_count': competencies.count() if hasattr(competencies, 'count') else len(competencies),
                'department': self.department.name if self.department else 'Mixed'
            },
            'competencies': [],
            'users': [],
            'matrix_data': []
        }

        # Add competency info
        for comp in competencies:
            matrix['competencies'].append({
                'id': comp.id,
                'name': comp.name,
                'category': comp.category.name if comp.category else 'N/A',
                'type': comp.get_competency_type_display()
            })

        # Add user data and proficiency levels
        for user in users:
            user_data = {
                'id': user.id,
                'name': user.get_full_name(),
                'email': user.email,
                'position': getattr(user, 'position_title', 'N/A'),
                'skills': {}
            }

            # Get user's competency assessments
            user_competencies = UserCompetency.objects.filter(
                user=user,
                competency__in=competencies
            ).select_related('competency')

            for user_comp in user_competencies:
                user_data['skills'][user_comp.competency_id] = {
                    'proficiency_level': user_comp.proficiency_level,
                    'current_level': user_comp.current_level,
                    'target_level': user_comp.target_level,
                    'status': self._get_proficiency_status(
                        user_comp.current_level,
                        user_comp.target_level
                    )
                }

            # Add missing competencies with 0 proficiency
            for comp in competencies:
                if comp.id not in user_data['skills']:
                    user_data['skills'][comp.id] = {
                        'proficiency_level': 0,
                        'current_level': 0,
                        'target_level': 0,
                        'status': 'not_assessed'
                    }

            matrix['users'].append(user_data)

        # Create matrix grid for easy visualization
        matrix['matrix_data'] = self._create_matrix_grid(matrix['users'], matrix['competencies'])

        # Add statistics
        matrix['statistics'] = self._calculate_matrix_statistics(matrix)

        return matrix

    def _create_matrix_grid(self, users, competencies):
        """Create 2D grid of skills."""
        grid = []

        for user in users:
            row = {
                'user_id': user['id'],
                'user_name': user['name'],
                'skills': []
            }

            for comp in competencies:
                skill_data = user['skills'].get(comp['id'], {})
                row['skills'].append({
                    'competency_id': comp['id'],
                    'level': skill_data.get('current_level', 0),
                    'status': skill_data.get('status', 'not_assessed')
                })

            grid.append(row)

        return grid

    def _calculate_matrix_statistics(self, matrix):
        """Calculate statistics from skill matrix."""
        total_assessments = 0
        total_proficiency = 0
        competency_coverage = {}

        for user in matrix['users']:
            for comp_id, skill in user['skills'].items():
                if skill['current_level'] > 0:
                    total_assessments += 1
                    total_proficiency += skill['current_level']

                    if comp_id not in competency_coverage:
                        competency_coverage[comp_id] = 0
                    competency_coverage[comp_id] += 1

        avg_proficiency = total_proficiency / total_assessments if total_assessments > 0 else 0

        # Calculate coverage percentage
        total_cells = matrix['metadata']['user_count'] * matrix['metadata']['competency_count']
        coverage_percentage = (total_assessments / total_cells * 100) if total_cells > 0 else 0

        return {
            'average_proficiency': round(avg_proficiency, 2),
            'coverage_percentage': round(coverage_percentage, 2),
            'total_assessments': total_assessments,
            'competency_coverage': competency_coverage
        }

    def _get_proficiency_status(self, current, target):
        """Get proficiency status based on current and target levels."""
        if current == 0:
            return 'not_assessed'
        elif current >= target:
            return 'proficient'
        elif current >= target * 0.7:
            return 'developing'
        else:
            return 'needs_development'

    def export_to_dict(self):
        """Export matrix to dictionary format."""
        return self.generate_matrix()


class SkillGapAnalyzer:
    """
    Analyzes skill gaps for individuals, teams, or departments.
    Identifies training needs and development priorities.
    """

    def __init__(self, user=None, users=None, department=None):
        """
        Initialize gap analyzer.

        Args:
            user: Single User instance for individual analysis
            users: Multiple User instances for team analysis
            department: Department instance for department analysis
        """
        self.user = user
        self.users = users
        self.department = department

    def analyze_individual_gaps(self, user=None):
        """
        Analyze skill gaps for an individual user.

        Args:
            user: User instance (optional, uses self.user if not provided)

        Returns:
            dict: Gap analysis results
        """
        target_user = user or self.user

        if not target_user:
            return {'error': 'No user specified'}

        # Get user's competency assessments
        user_competencies = UserCompetency.objects.filter(
            user=target_user
        ).select_related('competency')

        gaps = []
        strengths = []

        for user_comp in user_competencies:
            gap = user_comp.target_level - user_comp.current_level

            analysis = {
                'competency': user_comp.competency.name,
                'competency_id': user_comp.competency_id,
                'category': user_comp.competency.category.name if user_comp.competency.category else 'N/A',
                'current_level': user_comp.current_level,
                'target_level': user_comp.target_level,
                'gap': gap,
                'gap_percentage': (gap / user_comp.target_level * 100) if user_comp.target_level > 0 else 0,
                'priority': self._calculate_gap_priority(gap, user_comp.competency)
            }

            if gap > 0:
                gaps.append(analysis)
            else:
                strengths.append(analysis)

        # Sort gaps by priority
        gaps.sort(key=lambda x: x['priority'], reverse=True)

        # Get recommended training
        recommended_training = self._get_training_recommendations(gaps)

        return {
            'user': {
                'id': target_user.id,
                'name': target_user.get_full_name(),
                'position': getattr(target_user, 'position_title', 'N/A')
            },
            'gaps': gaps,
            'strengths': strengths,
            'summary': {
                'total_gaps': len(gaps),
                'critical_gaps': len([g for g in gaps if g['priority'] >= 8]),
                'total_strengths': len(strengths),
                'overall_readiness': self._calculate_readiness_score(user_competencies)
            },
            'recommended_training': recommended_training
        }

    def analyze_team_gaps(self, users=None):
        """
        Analyze collective skill gaps for a team.

        Args:
            users: List/QuerySet of User instances

        Returns:
            dict: Team gap analysis
        """
        target_users = users or self.users

        if not target_users:
            return {'error': 'No users specified'}

        # Aggregate competency data across team
        all_competencies = Competency.objects.filter(is_active=True)

        team_gaps = {}
        team_strengths = {}

        for comp in all_competencies:
            user_comps = UserCompetency.objects.filter(
                user__in=target_users,
                competency=comp
            )

            if not user_comps.exists():
                continue

            avg_current = user_comps.aggregate(avg=Avg('current_level'))['avg'] or 0
            avg_target = user_comps.aggregate(avg=Avg('target_level'))['avg'] or 0
            gap = avg_target - avg_current

            analysis = {
                'competency': comp.name,
                'competency_id': comp.id,
                'category': comp.category.name if comp.category else 'N/A',
                'team_avg_current': round(avg_current, 2),
                'team_avg_target': round(avg_target, 2),
                'gap': round(gap, 2),
                'users_assessed': user_comps.count(),
                'priority': self._calculate_gap_priority(gap, comp)
            }

            if gap > 0:
                team_gaps[comp.id] = analysis
            else:
                team_strengths[comp.id] = analysis

        # Sort by priority
        gaps_list = sorted(team_gaps.values(), key=lambda x: x['priority'], reverse=True)
        strengths_list = sorted(team_strengths.values(), key=lambda x: x['team_avg_current'], reverse=True)

        return {
            'team_size': target_users.count() if hasattr(target_users, 'count') else len(target_users),
            'gaps': gaps_list,
            'strengths': strengths_list,
            'summary': {
                'total_competencies_assessed': len(gaps_list) + len(strengths_list),
                'total_gaps': len(gaps_list),
                'critical_gaps': len([g for g in gaps_list if g['priority'] >= 8]),
                'total_strengths': len(strengths_list)
            },
            'recommended_team_training': self._get_training_recommendations(gaps_list[:10])
        }

    def analyze_department_gaps(self, department=None):
        """
        Analyze skill gaps at department level.

        Args:
            department: Department instance

        Returns:
            dict: Department gap analysis
        """
        target_dept = department or self.department

        if not target_dept:
            return {'error': 'No department specified'}

        from apps.accounts.models import User
        dept_users = User.objects.filter(department=target_dept, is_active=True)

        return self.analyze_team_gaps(dept_users)

    def _calculate_gap_priority(self, gap, competency):
        """
        Calculate priority score for a skill gap.

        Args:
            gap: Numeric gap value
            competency: Competency instance

        Returns:
            int: Priority score (1-10)
        """
        # Base priority on gap size
        if gap >= 3:
            priority = 10
        elif gap >= 2:
            priority = 8
        elif gap >= 1:
            priority = 6
        else:
            priority = 3

        # Adjust for competency importance
        if competency.is_critical:
            priority = min(10, priority + 2)

        return priority

    def _calculate_readiness_score(self, user_competencies):
        """Calculate overall readiness score based on competency gaps."""
        if not user_competencies.exists():
            return 0

        total_target = 0
        total_current = 0

        for user_comp in user_competencies:
            total_target += user_comp.target_level
            total_current += user_comp.current_level

        if total_target == 0:
            return 0

        readiness = (total_current / total_target) * 100
        return round(readiness, 2)

    def _get_training_recommendations(self, gaps):
        """
        Get training recommendations based on identified gaps.

        Args:
            gaps: List of gap analysis dicts

        Returns:
            List of recommended training resources
        """
        from .models import TrainingResource

        recommendations = []

        for gap in gaps[:5]:  # Top 5 gaps
            # Find relevant training resources
            resources = TrainingResource.objects.filter(
                required_competencies__id=gap.get('competency_id'),
                is_active=True
            ).distinct()[:3]

            if resources.exists():
                recommendations.append({
                    'competency': gap['competency'],
                    'gap': gap['gap'],
                    'priority': gap['priority'],
                    'training_resources': [
                        {
                            'id': r.id,
                            'title': r.title,
                            'type': r.get_type_display(),
                            'duration': r.duration_hours,
                            'link': r.link
                        }
                        for r in resources
                    ]
                })

        return recommendations

    def generate_development_plan(self, user=None):
        """
        Generate a comprehensive development plan based on gap analysis.

        Args:
            user: User instance

        Returns:
            dict: Development plan with prioritized actions
        """
        gap_analysis = self.analyze_individual_gaps(user)

        if 'error' in gap_analysis:
            return gap_analysis

        # Create prioritized development actions
        development_actions = []

        for gap in gap_analysis['gaps'][:10]:  # Top 10 gaps
            action = {
                'competency': gap['competency'],
                'current_level': gap['current_level'],
                'target_level': gap['target_level'],
                'gap': gap['gap'],
                'priority': gap['priority'],
                'timeline': self._estimate_timeline(gap['gap']),
                'recommended_approach': self._recommend_approach(gap)
            }
            development_actions.append(action)

        return {
            'user': gap_analysis['user'],
            'development_actions': development_actions,
            'summary': gap_analysis['summary'],
            'estimated_total_duration': sum(a['timeline'] for a in development_actions),
            'recommended_training': gap_analysis['recommended_training']
        }

    def _estimate_timeline(self, gap):
        """Estimate months needed to close gap."""
        if gap >= 3:
            return 6
        elif gap >= 2:
            return 4
        elif gap >= 1:
            return 2
        else:
            return 1

    def _recommend_approach(self, gap):
        """Recommend development approach based on gap."""
        if gap['gap'] >= 2:
            return 'Formal training + Mentorship + Practical projects'
        elif gap['gap'] >= 1:
            return 'Online courses + On-the-job practice'
        else:
            return 'Self-study + Peer learning'


# Helper functions
def generate_skill_matrix(users=None, department=None, competencies=None):
    """
    Quick function to generate skill matrix.

    Args:
        users: Users to include
        department: Department to analyze
        competencies: Specific competencies to include

    Returns:
        dict: Skill matrix
    """
    matrix = SkillMatrix(users=users, department=department, competencies=competencies)
    return matrix.generate_matrix()


def analyze_skill_gaps(user=None, users=None, department=None):
    """
    Quick function to analyze skill gaps.

    Args:
        user: Single user for individual analysis
        users: Multiple users for team analysis
        department: Department for department analysis

    Returns:
        dict: Gap analysis results
    """
    analyzer = SkillGapAnalyzer(user=user, users=users, department=department)

    if user:
        return analyzer.analyze_individual_gaps()
    elif department:
        return analyzer.analyze_department_gaps()
    elif users:
        return analyzer.analyze_team_gaps()
    else:
        return {'error': 'No target specified for analysis'}
