"""
AI-powered CV/Resume screening and candidate matching.
Uses NLP techniques for automated candidate evaluation and ranking.
"""
import re
import os
from decimal import Decimal
from typing import Dict, List, Tuple, Optional
from django.db.models import Q
from django.core.files.uploadedfile import UploadedFile

# Sentiment Analysis
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    VADER_AVAILABLE = True
except ImportError:
    VADER_AVAILABLE = False


class ResumeFileExtractor:
    """
    Rezyume fayllarından mətn çıxarır (PDF, DOCX, TXT).
    """

    @staticmethod
    def extract_text_from_file(file_path: str) -> str:
        """
        Fayldan mətn çıxarır.

        Args:
            file_path: Fayl yolu

        Returns:
            Çıxarılmış mətn
        """
        file_extension = os.path.splitext(file_path)[1].lower()

        try:
            if file_extension == '.pdf':
                return ResumeFileExtractor._extract_from_pdf(file_path)
            elif file_extension in ['.docx', '.doc']:
                return ResumeFileExtractor._extract_from_docx(file_path)
            elif file_extension == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                raise ValueError(f"Dəstəklənməyən fayl formatı: {file_extension}")
        except Exception as e:
            raise Exception(f"Fayldan mətn çıxarılarkən xəta: {str(e)}")

    @staticmethod
    def _extract_from_pdf(file_path: str) -> str:
        """PDF fayldan mətn çıxarır."""
        try:
            import PyPDF2
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except ImportError:
            # PyPDF2 yoxdursa, sadə oxuma
            raise ImportError("PyPDF2 kitabxanası quraşdırılmayıb. pip install PyPDF2")
        except Exception as e:
            raise Exception(f"PDF oxuma xətası: {str(e)}")

    @staticmethod
    def _extract_from_docx(file_path: str) -> str:
        """DOCX fayldan mətn çıxarır."""
        try:
            import docx
            doc = docx.Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except ImportError:
            raise ImportError("python-docx kitabxanası quraşdırılmayıb. pip install python-docx")
        except Exception as e:
            raise Exception(f"DOCX oxuma xətası: {str(e)}")

    @staticmethod
    def extract_from_uploaded_file(uploaded_file: UploadedFile) -> str:
        """
        Django UploadedFile obyektindən mətn çıxarır.

        Args:
            uploaded_file: Django yüklənmiş fayl obyekti

        Returns:
            Çıxarılmış mətn
        """
        import tempfile

        # Müvəqqəti faylda saxla və oxu
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            for chunk in uploaded_file.chunks():
                tmp_file.write(chunk)
            tmp_file_path = tmp_file.name

        try:
            text = ResumeFileExtractor.extract_text_from_file(tmp_file_path)
            return text
        finally:
            # Müvəqqəti faylı sil
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)


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
    def screen_application(application, resume_text: str, include_sentiment=True) -> Dict:
        """
        Screen an application using AI-powered analysis.

        Args:
            application: Application model instance
            resume_text: Extracted text from resume file
            include_sentiment: Include sentiment analysis of cover letter

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

        # Sentiment analysis of cover letter
        sentiment_analysis = None
        sentiment_feedback = []
        if include_sentiment and hasattr(application, 'cover_letter') and application.cover_letter:
            sentiment_analyzer = SentimentAnalyzer()
            sentiment_analysis = sentiment_analyzer.analyze_cover_letter(application.cover_letter)
            sentiment_feedback = sentiment_analyzer.generate_feedback(sentiment_analysis)

            # Adjust overall score based on sentiment (max ±5%)
            sentiment_adjustment = 0
            if sentiment_analysis['sentiment'] == 'positive' and sentiment_analysis['confidence'] > 60:
                sentiment_adjustment = 5
            elif sentiment_analysis['sentiment'] == 'negative':
                sentiment_adjustment = -5

            scores['original_score'] = scores['overall_score']
            scores['overall_score'] = min(100, max(0, scores['overall_score'] + sentiment_adjustment))
            scores['sentiment_adjustment'] = sentiment_adjustment

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

        result = {
            'parsed_cv': parsed_cv,
            'scores': scores,
            'recommendation': recommendation,
            'recommendation_text': recommendation_text,
            'screening_summary': AIScreeningEngine._generate_summary(scores, parsed_cv)
        }

        # Add sentiment analysis results if available
        if sentiment_analysis:
            result['sentiment_analysis'] = sentiment_analysis
            result['sentiment_feedback'] = sentiment_feedback

        return result

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


class SentimentAnalyzer:
    """
    Cover letter və motivasiya məktublarının sentiment analizi.
    VADER Sentiment Analysis istifadə edir.
    """

    def __init__(self):
        """Initialize sentiment analyzer."""
        if VADER_AVAILABLE:
            self.analyzer = SentimentIntensityAnalyzer()
        else:
            self.analyzer = None

    def analyze_cover_letter(self, cover_letter_text: str) -> Dict:
        """
        Cover letter-in sentiment analizini aparır.

        Args:
            cover_letter_text: Cover letter mətni

        Returns:
            Sentiment scores və qiymətləndirmə
        """
        if not cover_letter_text or not cover_letter_text.strip():
            return {
                'sentiment': 'neutral',
                'score': 0,
                'confidence': 0,
                'details': {},
                'interpretation': 'Mətn təqdim edilməyib'
            }

        if not self.analyzer:
            return {
                'sentiment': 'unavailable',
                'score': 0,
                'confidence': 0,
                'details': {},
                'interpretation': 'Sentiment analysis kitabxanası mövcud deyil'
            }

        # VADER sentiment scores
        scores = self.analyzer.polarity_scores(cover_letter_text)

        # Determine overall sentiment
        compound = scores['compound']

        if compound >= 0.05:
            sentiment = 'positive'
            interpretation = 'Pozitiv və həvəsli ton'
        elif compound <= -0.05:
            sentiment = 'negative'
            interpretation = 'Neqativ və ya şübhəli ton'
        else:
            sentiment = 'neutral'
            interpretation = 'Neytral və peşəkar ton'

        # Calculate confidence (0-100)
        confidence = min(abs(compound) * 100, 100)

        # Advanced analysis
        advanced_metrics = self._analyze_writing_quality(cover_letter_text)

        return {
            'sentiment': sentiment,
            'score': compound,  # -1 to +1
            'confidence': confidence,
            'details': {
                'positive': scores['pos'],
                'neutral': scores['neu'],
                'negative': scores['neg'],
                **advanced_metrics
            },
            'interpretation': interpretation
        }

    def _analyze_writing_quality(self, text: str) -> Dict:
        """
        Yazı keyfiyyətinin əlavə metrikləri.

        Args:
            text: Təhlil ediləcək mətn

        Returns:
            Keyfiyyət metriklərı
        """
        # Word count
        words = text.split()
        word_count = len(words)

        # Sentence count
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        sentence_count = len(sentences)

        # Average words per sentence
        avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0

        # Professional keywords
        professional_keywords = [
            'experience', 'skills', 'qualified', 'expertise', 'proficient',
            'accomplished', 'dedicated', 'motivated', 'passionate', 'collaborative',
            'innovative', 'results-driven', 'achievement', 'leadership'
        ]

        professional_keyword_count = sum(
            1 for keyword in professional_keywords
            if keyword.lower() in text.lower()
        )

        # Enthusiasm indicators
        enthusiasm_indicators = ['!', 'excited', 'eager', 'looking forward', 'thrilled']
        enthusiasm_score = sum(
            text.count(indicator) if indicator == '!' else (1 if indicator.lower() in text.lower() else 0)
            for indicator in enthusiasm_indicators
        )

        # Formality check (capitalization, no excessive slang)
        first_letter_caps = sum(1 for s in sentences if s and s[0].isupper())
        formality_score = (first_letter_caps / sentence_count * 100) if sentence_count > 0 else 0

        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_words_per_sentence': round(avg_words_per_sentence, 1),
            'professional_keywords': professional_keyword_count,
            'enthusiasm_score': enthusiasm_score,
            'formality_score': round(formality_score, 1),
            'readability': 'good' if 15 <= avg_words_per_sentence <= 25 else 'needs_improvement'
        }

    def generate_feedback(self, sentiment_result: Dict) -> List[str]:
        """
        Sentiment nəticəsinə əsasən feedback generasiya edir.

        Args:
            sentiment_result: analyze_cover_letter() nəticəsi

        Returns:
            Feedback tövsiyələri
        """
        feedback = []

        # Sentiment-based feedback
        if sentiment_result['sentiment'] == 'positive':
            feedback.append("✓ Pozitiv və həvəsli ton müsbət təəssürat yaradır")
        elif sentiment_result['sentiment'] == 'negative':
            feedback.append("⚠ Daha pozitiv və konstruktiv ton tövsiyə olunur")
        else:
            feedback.append("• Peşəkar və balanslaşdırılmış ton")

        details = sentiment_result.get('details', {})

        # Word count feedback
        word_count = details.get('word_count', 0)
        if word_count < 100:
            feedback.append("⚠ Cover letter çox qısa (min 150 söz tövsiyə olunur)")
        elif word_count > 500:
            feedback.append("⚠ Cover letter çox uzun (max 400 söz tövsiyə olunur)")
        else:
            feedback.append("✓ Optimal uzunluq")

        # Professional keywords
        prof_keywords = details.get('professional_keywords', 0)
        if prof_keywords < 3:
            feedback.append("⚠ Daha çox peşəkar açar sözlər istifadə edin")
        else:
            feedback.append(f"✓ {prof_keywords} peşəkar açar söz istifadə edilib")

        # Readability
        if details.get('readability') == 'needs_improvement':
            feedback.append("⚠ Cümlələrin uzunluğu optimallaşdırılmalıdır")

        # Enthusiasm
        enthusiasm = details.get('enthusiasm_score', 0)
        if enthusiasm == 0:
            feedback.append("💡 Həvəsinizi və motivasiyanızı daha aydın ifadə edin")
        elif enthusiasm > 5:
            feedback.append("⚠ Həvəsi daha balanslaşdırın (çox məcbur görünə bilər)")

        return feedback
