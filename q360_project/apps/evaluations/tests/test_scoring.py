"""
Comprehensive Tests for Evaluation Scoring Logic.
Tests weighted averages, decimal precision, and edge cases.
"""
from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import date, timedelta

from apps.accounts.models import User
from apps.departments.models import Organization, Department
from apps.evaluations.models import (
    EvaluationCampaign, QuestionCategory, Question,
    EvaluationAssignment, Response, EvaluationResult
)


class WeightValidationTests(TestCase):
    """Test weight field validation."""

    def setUp(self):
        """Set up test data."""
        self.organization = Organization.objects.create(
            name='Test Organization',
            short_name='TEST-ORG',
            code='TEST'
        )
        self.department = Department.objects.create(
            organization=self.organization,
            name='Test Dept',
            code='TEST'
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='test123',
            role='admin',
            department=self.department
        )

    def test_weights_sum_to_100(self):
        """Test that valid weights (summing to 100) are accepted."""
        campaign = EvaluationCampaign.objects.create(
            title='Test Campaign',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            weight_self=Decimal('20.00'),
            weight_supervisor=Decimal('50.00'),
            weight_peer=Decimal('20.00'),
            weight_subordinate=Decimal('10.00'),
            created_by=self.user
        )
        self.assertIsNotNone(campaign.pk)

    def test_weights_not_sum_to_100_raises_error(self):
        """Test that invalid weights (not summing to 100) raise ValidationError."""
        with self.assertRaises(ValidationError) as context:
            campaign = EvaluationCampaign(
                title='Test Campaign',
                start_date=date.today(),
                end_date=date.today() + timedelta(days=30),
                weight_self=Decimal('25.00'),
                weight_supervisor=Decimal('50.00'),
                weight_peer=Decimal('20.00'),
                weight_subordinate=Decimal('10.00'),  # Total = 105
                created_by=self.user
            )
            campaign.save()

        self.assertIn('weight_self', context.exception.message_dict)

    def test_weights_with_custom_distribution(self):
        """Test different valid weight distributions."""
        valid_distributions = [
            (30, 40, 20, 10),
            (0, 60, 30, 10),
            (10, 70, 10, 10),
            (25, 25, 25, 25),
        ]

        for self_w, super_w, peer_w, sub_w in valid_distributions:
            campaign = EvaluationCampaign.objects.create(
                title=f'Campaign {self_w}-{super_w}-{peer_w}-{sub_w}',
                start_date=date.today(),
                end_date=date.today() + timedelta(days=30),
                weight_self=Decimal(str(self_w)),
                weight_supervisor=Decimal(str(super_w)),
                weight_peer=Decimal(str(peer_w)),
                weight_subordinate=Decimal(str(sub_w)),
                created_by=self.user
            )
            self.assertIsNotNone(campaign.pk)


class ScoringCalculationTests(TestCase):
    """Test evaluation score calculations."""

    def setUp(self):
        """Set up complex evaluation scenario."""
        self.organization = Organization.objects.create(
            name='Test Organization',
            short_name='TEST-ORG',
            code='TEST'
        )
        self.department = Department.objects.create(
            organization=self.organization,
            name='Test Dept',
            code='TEST'
        )

        self.evaluatee = User.objects.create_user(
            username='evaluatee',
            email='evaluatee@test.com',
            password='test123',
            department=self.department
        )

        self.self_evaluator = self.evaluatee  # Self evaluation
        self.supervisor = User.objects.create_user(
            username='supervisor',
            email='supervisor@test.com',
            password='test123',
            role='manager',
            department=self.department
        )
        self.peer = User.objects.create_user(
            username='peer',
            email='peer@test.com',
            password='test123',
            department=self.department
        )
        self.subordinate = User.objects.create_user(
            username='subordinate',
            email='subordinate@test.com',
            password='test123',
            department=self.department,
            supervisor=self.evaluatee
        )

        # Create campaign with specific weights
        self.campaign = EvaluationCampaign.objects.create(
            title='Test Campaign',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            status='active',
            weight_self=Decimal('20.00'),
            weight_supervisor=Decimal('50.00'),
            weight_peer=Decimal('20.00'),
            weight_subordinate=Decimal('10.00'),
            created_by=self.supervisor
        )

        # Create question category and question
        self.category = QuestionCategory.objects.create(
            name='Test Category',
            order=1
        )
        self.question = Question.objects.create(
            category=self.category,
            text='Test question',
            question_type='scale',
            max_score=5,
            order=1
        )

    def create_assignment_with_responses(self, evaluator, relationship, scores):
        """Helper to create assignment with responses.

        NOTE: Creates one response per score with the SAME question.
        For multiple scores, create multiple questions first or pass average.
        """
        assignment = EvaluationAssignment.objects.create(
            campaign=self.campaign,
            evaluator=evaluator,
            evaluatee=self.evaluatee,
            relationship=relationship,
            status='completed'
        )

        # If multiple scores, create one response with average
        # (since unique_together prevents multiple responses for same question)
        if len(scores) > 1:
            avg_score = sum(scores) / len(scores)
            Response.objects.create(
                assignment=assignment,
                question=self.question,
                score=int(round(avg_score))
            )
        elif len(scores) == 1:
            Response.objects.create(
                assignment=assignment,
                question=self.question,
                score=scores[0]
            )

        return assignment

    def test_weighted_average_calculation(self):
        """Test weighted average calculation with all relationship types."""
        # Create evaluations with different scores
        self.create_assignment_with_responses(self.self_evaluator, 'self', [4, 4, 4])  # Avg: 4.0
        self.create_assignment_with_responses(self.supervisor, 'supervisor', [5, 5, 5])  # Avg: 5.0
        self.create_assignment_with_responses(self.peer, 'peer', [3, 3, 3])  # Avg: 3.0
        self.create_assignment_with_responses(self.subordinate, 'subordinate', [4, 4, 4])  # Avg: 4.0

        # Calculate result
        result, created = EvaluationResult.objects.get_or_create(
            campaign=self.campaign,
            evaluatee=self.evaluatee
        )
        result.calculate_scores()

        # Expected weighted score:
        # (4.0 * 20 + 5.0 * 50 + 3.0 * 20 + 4.0 * 10) / 100 = 4.3
        expected_score = Decimal('4.30')

        self.assertAlmostEqual(float(result.overall_score), float(expected_score), places=2)
        self.assertEqual(float(result.self_score), 4.0)
        self.assertEqual(float(result.supervisor_score), 5.0)
        self.assertEqual(float(result.peer_score), 3.0)
        self.assertEqual(float(result.subordinate_score), 4.0)

    def test_missing_relationship_scores(self):
        """Test calculation when some relationship types have no scores.

        CRITICAL: When relationships are missing, weights must be normalized to 100%.
        Example: If only supervisor (weight=50%) and peer (weight=20%) respond:
        - Total available weight = 50 + 20 = 70%
        - Normalized supervisor weight = (50/70) * 100 = 71.43%
        - Normalized peer weight = (20/70) * 100 = 28.57%
        - Overall score = (5.0 * 71.43 + 3.0 * 28.57) / 100 = 4.43
        """
        # Only supervisor and peer evaluate (no self and subordinate)
        self.create_assignment_with_responses(self.supervisor, 'supervisor', [5, 5])  # Avg: 5.0
        self.create_assignment_with_responses(self.peer, 'peer', [3, 3])  # Avg: 3.0

        result, created = EvaluationResult.objects.get_or_create(
            campaign=self.campaign,
            evaluatee=self.evaluatee
        )
        result.calculate_scores()

        # Expected with normalization:
        # total_weight = 50 + 20 = 70
        # normalized_supervisor = (50/70) * 100 = 71.43%
        # normalized_peer = (20/70) * 100 = 28.57%
        # overall = (5.0 * 71.43 + 3.0 * 28.57) / 100 = (357.15 + 85.71) / 100 = 4.43
        expected_score = Decimal('4.43')

        self.assertAlmostEqual(float(result.overall_score), float(expected_score), places=2)
        self.assertIsNone(result.self_score)
        self.assertEqual(float(result.supervisor_score), 5.0)
        self.assertEqual(float(result.peer_score), 3.0)
        self.assertIsNone(result.subordinate_score)

    def test_only_self_evaluation(self):
        """Test calculation with only self-evaluation."""
        self.create_assignment_with_responses(self.self_evaluator, 'self', [4, 4, 4])

        result, created = EvaluationResult.objects.get_or_create(
            campaign=self.campaign,
            evaluatee=self.evaluatee
        )
        result.calculate_scores()

        # With only self-evaluation, overall score should equal self score
        self.assertEqual(float(result.overall_score), 4.0)
        self.assertEqual(float(result.self_score), 4.0)

    def test_decimal_precision(self):
        """Test that decimal precision is maintained."""
        self.create_assignment_with_responses(self.supervisor, 'supervisor', [5, 4, 5, 4])  # Avg: 4.5

        result, created = EvaluationResult.objects.get_or_create(
            campaign=self.campaign,
            evaluatee=self.evaluatee
        )
        result.calculate_scores()

        # Check that we're using Decimal, not float
        self.assertIsInstance(result.overall_score, Decimal)
        self.assertIsInstance(result.supervisor_score, Decimal)

    def test_completion_rate_calculation(self):
        """Test completion rate percentage calculation."""
        # Create 4 assignments, only 2 completed
        EvaluationAssignment.objects.create(
            campaign=self.campaign,
            evaluator=self.self_evaluator,
            evaluatee=self.evaluatee,
            relationship='self',
            status='completed'
        )
        EvaluationAssignment.objects.create(
            campaign=self.campaign,
            evaluator=self.supervisor,
            evaluatee=self.evaluatee,
            relationship='supervisor',
            status='completed'
        )
        EvaluationAssignment.objects.create(
            campaign=self.campaign,
            evaluator=self.peer,
            evaluatee=self.evaluatee,
            relationship='peer',
            status='pending'
        )
        EvaluationAssignment.objects.create(
            campaign=self.campaign,
            evaluator=self.subordinate,
            evaluatee=self.evaluatee,
            relationship='subordinate',
            status='pending'
        )

        result, created = EvaluationResult.objects.get_or_create(
            campaign=self.campaign,
            evaluatee=self.evaluatee
        )
        result.calculate_scores()

        # Expected completion rate: 2/4 * 100 = 50%
        self.assertEqual(float(result.completion_rate), 50.0)

    def test_zero_weights_edge_case(self):
        """Test calculation when some weights are zero.

        CRITICAL: When a weight is 0, that relationship should be excluded from calculation.
        Example: peer weight = 0%, so peer evaluation should NOT affect the overall score.
        """
        # Create campaign with zero peer weight
        campaign = EvaluationCampaign.objects.create(
            title='Zero Peer Weight Campaign',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            weight_self=Decimal('30.00'),
            weight_supervisor=Decimal('60.00'),
            weight_peer=Decimal('0.00'),
            weight_subordinate=Decimal('10.00'),
            created_by=self.supervisor
        )

        # Create a separate question for this campaign
        question2 = Question.objects.create(
            category=self.category,
            text='Test question 2',
            question_type='scale',
            max_score=5,
            order=2
        )

        # Create assignments with new campaign
        assignment_self = EvaluationAssignment.objects.create(
            campaign=campaign,
            evaluator=self.self_evaluator,
            evaluatee=self.evaluatee,
            relationship='self',
            status='completed'
        )
        Response.objects.create(assignment=assignment_self, question=question2, score=4)

        assignment_supervisor = EvaluationAssignment.objects.create(
            campaign=campaign,
            evaluator=self.supervisor,
            evaluatee=self.evaluatee,
            relationship='supervisor',
            status='completed'
        )
        Response.objects.create(assignment=assignment_supervisor, question=question2, score=5)

        assignment_peer = EvaluationAssignment.objects.create(
            campaign=campaign,
            evaluator=self.peer,
            evaluatee=self.evaluatee,
            relationship='peer',
            status='completed'
        )
        Response.objects.create(assignment=assignment_peer, question=question2, score=3)  # Should be ignored (weight=0)

        assignment_subordinate = EvaluationAssignment.objects.create(
            campaign=campaign,
            evaluator=self.subordinate,
            evaluatee=self.evaluatee,
            relationship='subordinate',
            status='completed'
        )
        Response.objects.create(assignment=assignment_subordinate, question=question2, score=4)

        result, created = EvaluationResult.objects.get_or_create(
            campaign=campaign,
            evaluatee=self.evaluatee
        )
        result.calculate_scores()

        # Expected: Peer is ignored (weight=0), so only self, supervisor, subordinate count
        # total_weight = 30 + 60 + 10 = 100 (peer's 0 not counted)
        # normalized: self=30%, supervisor=60%, subordinate=10%
        # overall = (4*30 + 5*60 + 4*10) / 100 = (120 + 300 + 40) / 100 = 4.6
        expected_score = Decimal('4.60')
        self.assertIsNotNone(result.overall_score, "Overall score should not be None")
        self.assertAlmostEqual(float(result.overall_score), float(expected_score), places=2)
