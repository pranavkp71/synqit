import pytest
from synqit.analyzer import HeuristicAnalyzer

def test_auth_detection():
    diff = "some diff content"
    files = ["src/auth.py", "README.md"]
    analyzer = HeuristicAnalyzer(diff, files)
    analysis = analyzer.analyze()
    
    auth_results = [r for r in analysis.results if r.category == "Security"]
    assert len(auth_results) == 1
    assert auth_results[0].risk_level == "High"
    assert "auth.py" in auth_results[0].reason

def test_migration_detection():
    diff = "some diff content"
    files = ["app/migrations/0001_initial.py", "app/models.py"]
    analyzer = HeuristicAnalyzer(diff, files)
    analysis = analyzer.analyze()
    
    db_results = [r for r in analysis.results if r.category == "Database"]
    assert len(db_results) == 1
    assert db_results[0].risk_level == "Medium"

def test_missing_tests_detection():
    diff = "def new_func(): pass"
    files = ["synqit/new_feature.py"]
    analyzer = HeuristicAnalyzer(diff, files)
    analysis = analyzer.analyze()
    
    test_results = [r for r in analysis.results if r.category == "Testing"]
    assert len(test_results) == 1
    assert "no tests updated" in test_results[0].reason

def test_large_deletion_detection():
    # 60 lines deleted
    diff = "\n".join(["- line"] * 60) + "\n+ added line"
    files = ["big_file.py"]
    analyzer = HeuristicAnalyzer(diff, files)
    analysis = analyzer.analyze()
    
    risk_results = [r for r in analysis.results if r.category == "Risk"]
    assert len(risk_results) == 1
    assert "Large deletion" in risk_results[0].reason

def test_score_calculation():
    # 1 High (auth) + 1 Medium (migration)
    files = ["auth.py", "migrations/001.py"]
    analyzer = HeuristicAnalyzer("diff", files)
    analysis = analyzer.analyze()
    
    # High (40: Security) + Med (15: Database) + Med (15: Testing) = 70
    assert analysis.score == 70
    assert analysis.max_risk == "High"
