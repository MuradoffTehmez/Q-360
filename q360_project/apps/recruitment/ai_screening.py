"""
AI-powered CV/Resume screening and candidate matching.
Uses NLP techniques for automated candidate evaluation and ranking.
"""
import re
from decimal import Decimal
from typing import Dict, List, Tuple
from django.db.models import Q


class CVParser:
    """
    Parses CV/Resume files and extracts structured information.
    """

    # Common skill keywords by category
    SKILL_KEYWORDS = {
        'programming': [
            'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift',
            'kotlin', 'go', 'rust', 'typescript', 'scala', 'r', 'matlab'
        ],
        'frameworks': [
            'django', 'flask', 'react', 'angular', 'vue', 'spring', 'node.js',
            'express', 'fastapi', 'laravel', 'rails', '.net', 'tensorflow', 'pytorch'
        ],
        'databases': [
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
            'oracle', 'cassandra', 'dynamodb', 'firebase'
        ],
        'cloud': [
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'ci/cd',
            'terraform', 'ansible', 'cloudformation'
        ],
        'data_science': [
            'machine learning', 'deep learning', 'nlp', 'computer vision',
            'data analysis', 'statistics', 'pandas', 'numpy', 'scikit-learn'
        ],
        'soft_skills': [
            'leadership', 'communication', 'teamwork', 'problem solving',
            'analytical', 'project management', 'agile', 'scrum'
        ]
    }

    EDUCATION_LEVELS = {
        'phd': ['phd', 'ph.d', 'doctorate', 'doctoral'],
        'masters': ['master', 'msc', 'm.sc', 'ma', 'm.a', 'mba'],
        'bachelors': ['bachelor', 'bsc', 'b.sc', 'ba', 'b.a', 'bs'],
        'associate': ['associate'],
        'high_school': ['high school', 'secondary', 'diploma']
    }

    def __init__(self, resume_text: str):
        """
        Initialize parser with resume text.

        Args:
            resume_text: Extracted text from CV/resume file
        """
        self.text = resume_text.lower()
        self.original_text = resume_text

    def extract_skills(self) -> Dict[str, List[str]]:
        """
        Extract technical and soft skills from resume.

        Returns:
            Dictionary of categorized skills found in resume
        """
        found_skills = {}

        for category, keywords in self.SKILL_KEYWORDS.items():
            category_skills = []
            for skill in keywords:
                # Use word boundaries for accurate matching
                pattern = r'\b' + re.escape(skill.lower()) + r'\b'
                if re.search(pattern, self.text):
                    category_skills.append(skill)

            if category_skills:
                found_skills[category] = category_skills

        return found_skills

    def extract_education(self) -> List[Dict]:
        """
        Extract education information.

        Returns:
            List of education entries with level and institution
        """
        education_entries = []

        for level, keywords in self.EDUCATION_LEVELS.items():
            for keyword in keywords:
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, self.text):
                    education_entries.append({
                        'level': level,
                        'keyword': keyword
                    })
                    break  # Only add one entry per level

        return education_entries

    def extract_experience_years(self) -> int:
        """
        Estimate years of experience from resume.

        Returns:
            Estimated years of experience
        """
        # Look for patterns like "5 years", "5+ years", "5-7 years"
        patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp)',
            r'(?:experience|exp).*?(\d+)\+?\s*(?:years?|yrs?)',
        ]

        max_years = 0
        for pattern in patterns:
            matches = re.findall(pattern, self.text)
            if matches:
                years = [int(m) for m in matches if m.isdigit()]
                if years:
                    max_years = max(max_years, max(years))

        # Alternative: Count year ranges (e.g., 2015-2020)
        year_pattern = r'(20\d{2})\s*[-–]\s*(20\d{2}|present|current)'
        year_ranges = re.findall(year_pattern, self.text)

        if year_ranges and max_years == 0:
            total_years = 0
            from datetime import datetime
            current_year = datetime.now().year

            for start, end in year_ranges:
                start_year = int(start)
                end_year = current_year if end.lower() in ['present', 'current'] else int(end)
                total_years += (end_year - start_year)

            max_years = max(max_years, total_years)

        return max_years

    def extract_contact_info(self) -> Dict[str, str]:
        """
        Extract contact information.

        Returns:
            Dictionary with email, phone, etc.
        """
        contact_info = {}

        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, self.original_text)
        if emails:
            contact_info['email'] = emails[0]

        # Phone pattern (basic)
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, self.original_text)
        if phones:
            contact_info['phone'] = ''.join(phones[0]) if isinstance(phones[0], tuple) else phones[0]

        return contact_info


class CandidateScorer:
    """
    Scores candidates based on job requirements.
    """

    def __init__(self, job_posting):
        """
        Initialize scorer with job posting.

        Args:
            job_posting: JobPosting model instance
        """
        self.job = job_posting
        self.required_skills = self._extract_job_requirements()

    def _extract_job_requirements(self) -> Dict:
        """Extract required skills and qualifications from job posting."""
        requirements_text = (
            f"{self.job.requirements} {self.job.qualifications} {self.job.description}"
        ).lower()

        required_skills = {}
        for category, keywords in CVParser.SKILL_KEYWORDS.items():
            category_skills = []
            for skill in keywords:
                if skill in requirements_text:
                    category_skills.append(skill)
            if category_skills:
                required_skills[category] = category_skills

        return required_skills

    def score_application(self, application, parsed_cv: Dict) -> Dict:
        """
        Score an application based on CV analysis.

        Args:
            application: Application model instance
            parsed_cv: Parsed CV data from CVParser

        Returns:
            Dictionary with scores and match details
        """
        scores = {
            'skills_match': 0,
            'experience_match': 0,
            'education_match': 0,
            'overall_score': 0,
            'match_details': {}
        }

        # 1. Skills Match (50% weight)
        skills_score = self._calculate_skills_match(parsed_cv.get('skills', {}))
        scores['skills_match'] = skills_score

        # 2. Experience Match (30% weight)
        experience_score = self._calculate_experience_match(
            parsed_cv.get('experience_years', 0)
        )
        scores['experience_match'] = experience_score

        # 3. Education Match (20% weight)
        education_score = self._calculate_education_match(
            parsed_cv.get('education', [])
        )
        scores['education_match'] = education_score

        # Calculate overall weighted score
        scores['overall_score'] = (
            skills_score * 0.5 +
            experience_score * 0.3 +
            education_score * 0.2
        )

        # Add match details
        scores['match_details'] = self._generate_match_details(parsed_cv)

        return scores

    def _calculate_skills_match(self, candidate_skills: Dict) -> float:
        """Calculate skill match percentage."""
        if not self.required_skills:
            return 50.0  # Neutral score if no specific requirements

        total_required = sum(len(skills) for skills in self.required_skills.values())
        if total_required == 0:
            return 50.0

        matched_skills = 0
        for category, required in self.required_skills.items():
            candidate_category = candidate_skills.get(category, [])
            matched_skills += len(set(required) & set(candidate_category))

        match_percentage = (matched_skills / total_required) * 100
        return min(100.0, match_percentage)

    def _calculate_experience_match(self, candidate_years: int) -> float:
        """Calculate experience match score."""
        # Map experience level to expected years
        experience_map = {
            'entry': (0, 1),
            'junior': (1, 3),
            'mid': (3, 6),
            'senior': (6, 10),
            'lead': (8, 15),
            'manager': (10, 999)
        }

        min_years, max_years = experience_map.get(
            self.job.experience_level,
            (0, 999)
        )

        if min_years <= candidate_years <= max_years:
            return 100.0
        elif candidate_years < min_years:
            # Penalize lack of experience
            shortage = min_years - candidate_years
            return max(0, 100 - (shortage * 20))
        else:
            # Minor penalty for overqualification
            excess = candidate_years - max_years
            return max(70, 100 - (excess * 5))

    def _calculate_education_match(self, candidate_education: List) -> float:
        """Calculate education match score."""
        # Map experience level to typical education requirement
        education_requirements = {
            'entry': ['bachelors', 'associate'],
            'junior': ['bachelors'],
            'mid': ['bachelors', 'masters'],
            'senior': ['bachelors', 'masters'],
            'lead': ['bachelors', 'masters', 'phd'],
            'manager': ['bachelors', 'masters', 'phd']
        }

        required_levels = education_requirements.get(
            self.job.experience_level,
            ['bachelors']
        )

        candidate_levels = [edu['level'] for edu in candidate_education]

        # Check if candidate meets any required level
        if any(level in candidate_levels for level in required_levels):
            # Bonus for higher education
            if 'phd' in candidate_levels:
                return 100.0
            elif 'masters' in candidate_levels:
                return 95.0
            elif 'bachelors' in candidate_levels:
                return 90.0
            else:
                return 75.0
        else:
            return 50.0

    def _generate_match_details(self, parsed_cv: Dict) -> Dict:
        """Generate detailed matching information."""
        candidate_skills = parsed_cv.get('skills', {})

        # Find matching and missing skills
        matching_skills = []
        missing_skills = []

        for category, required in self.required_skills.items():
            candidate_category = candidate_skills.get(category, [])
            matching = set(required) & set(candidate_category)
            missing = set(required) - set(candidate_category)

            matching_skills.extend(matching)
            missing_skills.extend(missing)

        return {
            'matching_skills': matching_skills,
            'missing_skills': missing_skills,
            'total_skills_found': sum(len(skills) for skills in candidate_skills.values()),
            'education_levels': [edu['level'] for edu in parsed_cv.get('education', [])],
            'experience_years': parsed_cv.get('experience_years', 0)
        }


class AIScreeningEngine:
    """
    Main AI screening engine that coordinates CV parsing and candidate scoring.
    """

    @staticmethod
    def screen_application(application, resume_text: str) -> Dict:
        """
        Screen an application using AI-powered analysis.

        Args:
            application: Application model instance
            resume_text: Extracted text from resume file

        Returns:
            Dictionary with screening results and recommendations
        """
        # Parse CV
        parser = CVParser(resume_text)
        parsed_cv = {
            'skills': parser.extract_skills(),
            'education': parser.extract_education(),
            'experience_years': parser.extract_experience_years(),
            'contact_info': parser.extract_contact_info()
        }

        # Score candidate
        scorer = CandidateScorer(application.job_posting)
        scores = scorer.score_application(application, parsed_cv)

        # Generate recommendation
        overall_score = scores['overall_score']
        if overall_score >= 75:
            recommendation = 'strong_yes'
            recommendation_text = 'Güclü namizəd - Müsahibəyə dəvət edin'
        elif overall_score >= 60:
            recommendation = 'yes'
            recommendation_text = 'Uyğun namizəd - Baxış tövsiyə olunur'
        elif overall_score >= 45:
            recommendation = 'maybe'
            recommendation_text = 'Potensial namizəd - Əlavə baxış lazımdır'
        else:
            recommendation = 'no'
            recommendation_text = 'Uyğun deyil'

        return {
            'parsed_cv': parsed_cv,
            'scores': scores,
            'recommendation': recommendation,
            'recommendation_text': recommendation_text,
            'screening_summary': AIScreeningEngine._generate_summary(scores, parsed_cv)
        }

    @staticmethod
    def _generate_summary(scores: Dict, parsed_cv: Dict) -> str:
        """Generate human-readable screening summary."""
        summary_parts = []

        # Skills summary
        skills_score = scores['skills_match']
        if skills_score >= 75:
            summary_parts.append(f"✓ Bacarıqlar yüksək uyğunluqdadır ({skills_score:.0f}%)")
        elif skills_score >= 50:
            summary_parts.append(f"~ Bacarıqlar qismən uyğundur ({skills_score:.0f}%)")
        else:
            summary_parts.append(f"✗ Bacarıqlar zəif uyğunluqdadır ({skills_score:.0f}%)")

        # Experience summary
        exp_years = parsed_cv.get('experience_years', 0)
        exp_score = scores['experience_match']
        summary_parts.append(f"Təcrübə: {exp_years} il (uyğunluq: {exp_score:.0f}%)")

        # Education summary
        education = parsed_cv.get('education', [])
        if education:
            levels = [edu['level'] for edu in education]
            summary_parts.append(f"Təhsil: {', '.join(levels).title()}")

        # Match details
        match_details = scores.get('match_details', {})
        matching_skills = match_details.get('matching_skills', [])
        missing_skills = match_details.get('missing_skills', [])

        if matching_skills:
            summary_parts.append(f"Uyğun bacarıqlar: {len(matching_skills)}")
        if missing_skills:
            summary_parts.append(f"Çatışmayan bacarıqlar: {len(missing_skills)}")

        return "\n".join(summary_parts)

    @staticmethod
    def batch_screen_applications(job_posting, limit=None):
        """
        Screen multiple applications for a job posting.

        Args:
            job_posting: JobPosting instance
            limit: Maximum number of applications to screen

        Returns:
            List of applications with screening results
        """
        from .models import Application

        applications = Application.objects.filter(
            job_posting=job_posting,
            status='received'
        ).order_by('-applied_at')

        if limit:
            applications = applications[:limit]

        screened_results = []

        for application in applications:
            # In real implementation, extract text from resume file
            # For now, use description as placeholder
            resume_text = f"{application.cover_letter} {application.current_position}"

            try:
                result = AIScreeningEngine.screen_application(application, resume_text)
                result['application'] = application
                screened_results.append(result)
            except Exception as e:
                # Log error but continue processing
                print(f"Error screening application {application.id}: {e}")
                continue

        # Sort by overall score
        screened_results.sort(
            key=lambda x: x['scores']['overall_score'],
            reverse=True
        )

        return screened_results
