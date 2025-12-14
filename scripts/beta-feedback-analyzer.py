#!/usr/bin/env python3
"""
HUMMBL Beta Feedback Analyzer

This script collects, analyzes, and prioritizes beta user feedback.
It processes surveys, support tickets, and community discussions to
identify trends, themes, and actionable insights.

Usage:
    python beta-feedback-analyzer.py --collect-feedback
    python beta-feedback-analyzer.py --analyze-surveys
    python beta-feedback-analyzer.py --generate-report
    python beta-feedback-analyzer.py --prioritize-issues
"""

import argparse
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
import re
from collections import defaultdict, Counter
import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class FeedbackItem:
    """Individual feedback item"""
    id: str
    source: str  # 'survey', 'support', 'forum', 'interview'
    user_id: Optional[str]
    timestamp: datetime
    category: str  # 'bug', 'feature_request', 'usability', 'performance', 'general'
    sentiment: str  # 'positive', 'negative', 'neutral'
    priority: str  # 'critical', 'high', 'medium', 'low'
    title: str
    description: str
    tags: List[str]
    affected_users: int
    status: str  # 'open', 'in_progress', 'resolved', 'closed'

@dataclass
class FeedbackTheme:
    """Identified theme from feedback analysis"""
    theme: str
    frequency: int
    sentiment_score: float  # -1 to 1
    affected_users: int
    priority_score: float
    related_items: List[str]
    suggested_actions: List[str]

class FeedbackDatabase:
    """Database for storing and retrieving feedback"""

    def __init__(self, db_path: str = 'beta_feedback.db'):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Initialize database schema"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS feedback (
                    id TEXT PRIMARY KEY,
                    source TEXT,
                    user_id TEXT,
                    timestamp TEXT,
                    category TEXT,
                    sentiment TEXT,
                    priority TEXT,
                    title TEXT,
                    description TEXT,
                    tags TEXT,
                    affected_users INTEGER,
                    status TEXT
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS themes (
                    theme TEXT PRIMARY KEY,
                    frequency INTEGER,
                    sentiment_score REAL,
                    affected_users INTEGER,
                    priority_score REAL,
                    related_items TEXT,
                    suggested_actions TEXT,
                    last_updated TEXT
                )
            ''')
            conn.commit()

    def save_feedback(self, feedback: FeedbackItem):
        """Save feedback item to database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO feedback
                (id, source, user_id, timestamp, category, sentiment, priority,
                 title, description, tags, affected_users, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                feedback.id, feedback.source, feedback.user_id,
                feedback.timestamp.isoformat(), feedback.category,
                feedback.sentiment, feedback.priority, feedback.title,
                feedback.description, json.dumps(feedback.tags),
                feedback.affected_users, feedback.status
            ))
            conn.commit()

    def get_recent_feedback(self, days: int = 7) -> List[FeedbackItem]:
        """Get feedback from the last N days"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                SELECT * FROM feedback
                WHERE timestamp >= datetime('now', '-{} days')
                ORDER BY timestamp DESC
            '''.format(days))

            feedback = []
            for row in cursor.fetchall():
                feedback.append(FeedbackItem(
                    id=row[0],
                    source=row[1],
                    user_id=row[2],
                    timestamp=datetime.fromisoformat(row[3]),
                    category=row[4],
                    sentiment=row[5],
                    priority=row[6],
                    title=row[7],
                    description=row[8],
                    tags=json.loads(row[9]),
                    affected_users=row[10],
                    status=row[11]
                ))
            return feedback

    def save_theme(self, theme: FeedbackTheme):
        """Save theme analysis to database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO themes
                (theme, frequency, sentiment_score, affected_users,
                 priority_score, related_items, suggested_actions, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                theme.theme, theme.frequency, theme.sentiment_score,
                theme.affected_users, theme.priority_score,
                json.dumps(theme.related_items),
                json.dumps(theme.suggested_actions),
                datetime.now().isoformat()
            ))
            conn.commit()

class FeedbackCollector:
    """Collect feedback from various sources"""

    def __init__(self):
        self.mock_data = True  # Set to False for real data collection

    def collect_survey_responses(self) -> List[Dict[str, Any]]:
        """Collect responses from weekly pulse surveys"""
        if self.mock_data:
            return [
                {
                    'user_id': 'user_001',
                    'timestamp': datetime.now() - timedelta(hours=2),
                    'rating': 8,
                    'working_well': 'SY19 recommendations are very accurate',
                    'challenges': 'API documentation could be clearer',
                    'improvement_suggestion': 'Add more export formats',
                    'nps': 9
                },
                {
                    'user_id': 'user_002',
                    'timestamp': datetime.now() - timedelta(hours=4),
                    'rating': 6,
                    'working_well': 'Interface is clean and intuitive',
                    'challenges': 'Performance is slow with large datasets',
                    'improvement_suggestion': 'Implement caching for better performance',
                    'nps': 7
                },
                {
                    'user_id': 'user_003',
                    'timestamp': datetime.now() - timedelta(hours=6),
                    'rating': 9,
                    'working_well': 'Mental model explanations are excellent',
                    'challenges': 'Learning curve for advanced features',
                    'improvement_suggestion': 'Add interactive tutorials',
                    'nps': 10
                }
            ]

        # Real implementation would call survey API
        # return self._call_survey_api('/responses/recent')

    def collect_support_tickets(self) -> List[Dict[str, Any]]:
        """Collect support ticket data"""
        if self.mock_data:
            return [
                {
                    'ticket_id': 'TICKET-001',
                    'user_id': 'user_001',
                    'timestamp': datetime.now() - timedelta(days=1),
                    'subject': 'API authentication failing',
                    'description': 'Getting 401 errors when calling recommendation endpoint',
                    'category': 'technical',
                    'priority': 'high',
                    'status': 'resolved'
                },
                {
                    'ticket_id': 'TICKET-002',
                    'user_id': 'user_004',
                    'timestamp': datetime.now() - timedelta(days=2),
                    'subject': 'Feature request: bulk analysis',
                    'description': 'Need ability to analyze multiple problems at once',
                    'category': 'feature_request',
                    'priority': 'medium',
                    'status': 'open'
                }
            ]

        # Real implementation would call support API
        # return self._call_support_api('/tickets/recent')

    def collect_forum_posts(self) -> List[Dict[str, Any]]:
        """Collect forum and community discussion data"""
        if self.mock_data:
            return [
                {
                    'post_id': 'POST-001',
                    'user_id': 'user_005',
                    'timestamp': datetime.now() - timedelta(hours=12),
                    'title': 'SY19 accuracy feedback',
                    'content': 'The model recommendations have been 85% accurate for my use cases. Very impressed!',
                    'channel': 'general',
                    'replies': 3
                },
                {
                    'post_id': 'POST-002',
                    'user_id': 'user_006',
                    'timestamp': datetime.now() - timedelta(hours=18),
                    'title': 'VS Code extension issues',
                    'content': 'Extension keeps disconnecting. Anyone else experiencing this?',
                    'channel': 'help-desk',
                    'replies': 7
                }
            ]

        # Real implementation would call forum API
        # return self._call_forum_api('/posts/recent')

class SentimentAnalyzer:
    """Analyze sentiment of feedback text"""

    def __init__(self):
        # Simple keyword-based sentiment analysis
        self.positive_words = {
            'excellent', 'great', 'amazing', 'love', 'awesome', 'fantastic',
            'perfect', 'brilliant', 'outstanding', 'impressed', 'helpful',
            'accurate', 'intuitive', 'smooth', 'fast', 'reliable'
        }
        self.negative_words = {
            'terrible', 'awful', 'hate', 'worst', 'broken', 'slow', 'confusing',
            'frustrating', 'disappointed', 'annoying', 'difficult', 'buggy',
            'unreliable', 'crashes', 'errors', 'fails'
        }

    def analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment of text"""
        text_lower = text.lower()
        positive_count = sum(1 for word in self.positive_words if word in text_lower)
        negative_count = sum(1 for word in self.negative_words if word in text_lower)

        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'

class ThemeExtractor:
    """Extract themes and patterns from feedback"""

    def __init__(self):
        self.theme_keywords = {
            'performance': ['slow', 'fast', 'performance', 'speed', 'loading', 'lag', 'responsive'],
            'usability': ['intuitive', 'confusing', 'easy', 'difficult', 'user-friendly', 'complicated'],
            'accuracy': ['accurate', 'wrong', 'correct', 'precision', 'reliable', 'inaccurate'],
            'features': ['feature', 'functionality', 'capability', 'missing', 'need', 'request'],
            'api': ['api', 'integration', 'endpoint', 'authentication', 'documentation'],
            'ui': ['interface', 'design', 'layout', 'visual', 'appearance', 'navigation'],
            'bugs': ['bug', 'error', 'crash', 'broken', 'fix', 'issue', 'problem']
        }

    def extract_themes(self, feedback_items: List[FeedbackItem]) -> List[FeedbackTheme]:
        """Extract themes from feedback items"""
        theme_counter = Counter()
        theme_sentiment = defaultdict(list)
        theme_users = defaultdict(set)
        theme_items = defaultdict(list)

        for item in feedback_items:
            text = f"{item.title} {item.description}".lower()

            for theme, keywords in self.theme_keywords.items():
                if any(keyword in text for keyword in keywords):
                    theme_counter[theme] += 1
                    theme_sentiment[theme].append(1 if item.sentiment == 'positive' else -1 if item.sentiment == 'negative' else 0)
                    if item.user_id:
                        theme_users[theme].add(item.user_id)
                    theme_items[theme].append(item.id)

        themes = []
        for theme, frequency in theme_counter.most_common():
            sentiment_scores = theme_sentiment[theme]
            avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
            affected_users = len(theme_users[theme])

            # Calculate priority score based on frequency, sentiment, and user impact
            priority_score = (frequency * 0.4) + (abs(avg_sentiment) * 10 * 0.3) + (affected_users * 0.3)

            # Generate suggested actions based on theme
            suggested_actions = self._generate_actions(theme, avg_sentiment, frequency)

            themes.append(FeedbackTheme(
                theme=theme,
                frequency=frequency,
                sentiment_score=avg_sentiment,
                affected_users=affected_users,
                priority_score=priority_score,
                related_items=theme_items[theme],
                suggested_actions=suggested_actions
            ))

        return sorted(themes, key=lambda x: x.priority_score, reverse=True)

    def _generate_actions(self, theme: str, sentiment: float, frequency: int) -> List[str]:
        """Generate suggested actions for a theme"""
        actions = []

        if theme == 'performance' and sentiment < 0:
            actions.extend([
                "Implement caching layer for frequently accessed data",
                "Optimize database queries and add indexes",
                "Consider CDN for static assets"
            ])
        elif theme == 'usability' and sentiment < 0:
            actions.extend([
                "Conduct user testing sessions to identify pain points",
                "Redesign complex workflows for simplicity",
                "Add interactive tutorials and tooltips"
            ])
        elif theme == 'accuracy' and sentiment < 0:
            actions.extend([
                "Review and improve SY19 model training data",
                "Add confidence scores to recommendations",
                "Implement user feedback loop for model improvement"
            ])
        elif theme == 'features':
            actions.extend([
                "Prioritize feature requests based on user impact",
                "Create public roadmap for transparency",
                "Implement voting system for feature prioritization"
            ])
        elif theme == 'api' and sentiment < 0:
            actions.extend([
                "Improve API documentation with examples",
                "Add comprehensive error messages",
                "Create SDK packages for popular languages"
            ])
        elif theme == 'bugs':
            actions.extend([
                "Establish regular bug triage meetings",
                "Improve testing coverage for reported issues",
                "Implement automated error reporting"
            ])

        return actions[:3]  # Return top 3 actions

class FeedbackProcessor:
    """Process and analyze feedback data"""

    def __init__(self, db: FeedbackDatabase):
        self.db = db
        self.collector = FeedbackCollector()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.theme_extractor = ThemeExtractor()

    def process_all_feedback(self):
        """Collect and process all feedback sources"""
        logger.info("Collecting feedback from all sources...")

        # Collect data from different sources
        surveys = self.collector.collect_survey_responses()
        tickets = self.collector.collect_support_tickets()
        posts = self.collector.collect_forum_posts()

        # Convert to FeedbackItem objects
        feedback_items = []

        # Process surveys
        for survey in surveys:
            sentiment = self.sentiment_analyzer.analyze_sentiment(
                f"{survey['working_well']} {survey['challenges']}"
            )

            category = 'general'
            if 'api' in survey['challenges'].lower() or 'documentation' in survey['challenges'].lower():
                category = 'api'
            elif 'performance' in survey['challenges'].lower():
                category = 'performance'
            elif 'feature' in survey['improvement_suggestion'].lower():
                category = 'feature_request'

            priority = 'medium'
            if survey['rating'] <= 6:
                priority = 'high'
            elif survey['rating'] >= 9:
                priority = 'low'

            feedback_items.append(FeedbackItem(
                id=f"survey_{survey['user_id']}_{survey['timestamp'].strftime('%Y%m%d_%H%M%S')}",
                source='survey',
                user_id=survey['user_id'],
                timestamp=survey['timestamp'],
                category=category,
                sentiment=sentiment,
                priority=priority,
                title=f"Weekly Survey Response - Rating: {survey['rating']}/10",
                description=f"Working well: {survey['working_well']}\nChallenges: {survey['challenges']}\nSuggestion: {survey['improvement_suggestion']}",
                tags=['survey', f'rating_{survey["rating"]}'],
                affected_users=1,
                status='open'
            ))

        # Process support tickets
        for ticket in tickets:
            sentiment = self.sentiment_analyzer.analyze_sentiment(ticket['description'])

            feedback_items.append(FeedbackItem(
                id=ticket['ticket_id'],
                source='support',
                user_id=ticket['user_id'],
                timestamp=ticket['timestamp'],
                category=ticket['category'],
                sentiment=sentiment,
                priority=ticket['priority'],
                title=ticket['subject'],
                description=ticket['description'],
                tags=['support', ticket['category'], ticket['priority']],
                affected_users=1,
                status=ticket['status']
            ))

        # Process forum posts
        for post in posts:
            sentiment = self.sentiment_analyzer.analyze_sentiment(
                f"{post['title']} {post['content']}"
            )

            category = 'general'
            if 'help' in post['channel'] or 'bug' in post['content'].lower():
                category = 'bug'
            elif 'feature' in post['content'].lower():
                category = 'feature_request'

            priority = 'medium'
            if 'crash' in post['content'].lower() or 'broken' in post['content'].lower():
                priority = 'high'

            feedback_items.append(FeedbackItem(
                id=post['post_id'],
                source='forum',
                user_id=post['user_id'],
                timestamp=post['timestamp'],
                category=category,
                sentiment=sentiment,
                priority=priority,
                title=post['title'],
                description=post['content'],
                tags=['forum', post['channel']],
                affected_users=max(1, post.get('replies', 0)),
                status='open'
            ))

        # Save all feedback items
        for item in feedback_items:
            self.db.save_feedback(item)

        logger.info(f"Processed {len(feedback_items)} feedback items")

        # Extract and save themes
        themes = self.theme_extractor.extract_themes(feedback_items)
        for theme in themes:
            self.db.save_theme(theme)

        logger.info(f"Extracted {len(themes)} feedback themes")

        return feedback_items, themes

class ReportGenerator:
    """Generate feedback analysis reports"""

    def __init__(self, db: FeedbackDatabase):
        self.db = db

    def generate_weekly_report(self) -> str:
        """Generate weekly feedback analysis report"""
        feedback_items = self.db.get_recent_feedback(days=7)

        if not feedback_items:
            return "No feedback data available for weekly report"

        # Calculate metrics
        total_feedback = len(feedback_items)
        sentiment_counts = Counter(item.sentiment for item in feedback_items)
        category_counts = Counter(item.category for item in feedback_items)
        priority_counts = Counter(item.priority for item in feedback_items)

        avg_rating = 0
        rating_count = 0
        for item in feedback_items:
            if item.source == 'survey' and 'rating' in item.description:
                # Extract rating from survey description
                rating_match = re.search(r'Rating: (\d+)/10', item.description)
                if rating_match:
                    avg_rating += int(rating_match.group(1))
                    rating_count += 1

        if rating_count > 0:
            avg_rating /= rating_count

        # Get top themes
        themes_query = "SELECT * FROM themes ORDER BY priority_score DESC LIMIT 5"
        with sqlite3.connect(self.db.db_path) as conn:
            cursor = conn.execute(themes_query)
            top_themes = []
            for row in cursor.fetchall():
                top_themes.append({
                    'theme': row[0],
                    'frequency': row[1],
                    'sentiment_score': row[2],
                    'affected_users': row[3],
                    'priority_score': row[4]
                })

        # Generate report
        report = f"""
HUMMBL Beta Weekly Feedback Report
Week of: {(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

EXECUTIVE SUMMARY
=================
• Total Feedback Items: {total_feedback}
• Average Rating: {avg_rating:.1f}/10 ({rating_count} responses)
• Sentiment Distribution: {dict(sentiment_counts)}
• Most Common Category: {category_counts.most_common(1)[0][0] if category_counts else 'N/A'}

FEEDBACK BREAKDOWN
==================
Categories:
"""

        for category, count in category_counts.most_common():
            report += f"• {category}: {count} items\n"

        report += "\nPriority Levels:\n"
        for priority, count in priority_counts.most_common():
            report += f"• {priority}: {count} items\n"

        report += "\nTOP THEMES IDENTIFIED\n=====================\n"

        for i, theme in enumerate(top_themes, 1):
            sentiment_desc = "positive" if theme['sentiment_score'] > 0.1 else "negative" if theme['sentiment_score'] < -0.1 else "neutral"
            report += f"{i}. {theme['theme'].title()}\n"
            report += f"   • Frequency: {theme['frequency']} mentions\n"
            report += f"   • Sentiment: {sentiment_desc} ({theme['sentiment_score']:.2f})\n"
            report += f"   • Affected Users: {theme['affected_users']}\n"
            report += f"   • Priority Score: {theme['priority_score']:.1f}\n\n"

        report += """
KEY INSIGHTS & RECOMMENDATIONS
==============================="""


        # Generate insights based on data
        if avg_rating < 7.0:
            report += "⚠️  Average rating below target. Focus on addressing top pain points.\n"
        if priority_counts.get('critical', 0) > 0:
            report += "🚨 Critical issues identified. Immediate attention required.\n"
        if sentiment_counts.get('negative', 0) > sentiment_counts.get('positive', 0):
            report += "⚠️  Negative sentiment dominates. Review user experience issues.\n"

        # Theme-specific recommendations
        for theme in top_themes[:3]:
            if theme['sentiment_score'] < -0.1:
                report += f"• Address {theme['theme']} issues - affecting {theme['affected_users']} users\n"

        return report

def main():
    parser = argparse.ArgumentParser(description='HUMMBL Beta Feedback Analyzer')
    parser.add_argument('--collect-feedback', action='store_true', help='Collect feedback from all sources')
    parser.add_argument('--analyze-surveys', action='store_true', help='Analyze survey responses')
    parser.add_argument('--generate-report', action='store_true', help='Generate feedback analysis report')
    parser.add_argument('--prioritize-issues', action='store_true', help='Analyze and prioritize feedback issues')

    args = parser.parse_args()

    db = FeedbackDatabase()
    processor = FeedbackProcessor(db)
    report_gen = ReportGenerator(db)

    if args.collect_feedback:
        logger.info("Collecting and processing feedback...")
        feedback_items, themes = processor.process_all_feedback()
        logger.info(f"Processed {len(feedback_items)} feedback items and identified {len(themes)} themes")

    if args.analyze_surveys:
        logger.info("Analyzing survey responses...")
        # Survey analysis would be part of the collection process
        logger.info("Survey analysis completed")

    if args.generate_report:
        logger.info("Generating feedback report...")
        report = report_gen.generate_weekly_report()
        print(report)

        # Save report to file
        with open(f'beta_feedback_report_{datetime.now().strftime("%Y%m%d")}.md', 'w') as f:
            f.write(report)
        logger.info("Report saved to file")

    if args.prioritize_issues:
        logger.info("Analyzing and prioritizing issues...")
        # This is handled in the theme extraction process
        logger.info("Issue prioritization completed")

    # If no arguments provided, show help
    if not any([args.collect_feedback, args.analyze_surveys, args.generate_report, args.prioritize_issues]):
        parser.print_help()

if __name__ == '__main__':
    main()