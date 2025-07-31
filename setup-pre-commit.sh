#!/bin/bash
# Setup script for pre-commit hooks in LaTeX Formatter project

set -e

echo "🚀 Setting up pre-commit hooks for LaTeX Formatter..."

# Check if pre-commit is installed
if ! command -v pre-commit &> /dev/null; then
    echo "📦 Installing pre-commit..."
    pip install pre-commit
else
    echo "✅ pre-commit is already installed"
fi

# Install the pre-commit hooks
echo "🔧 Installing pre-commit hooks..."
pre-commit install

# Install commit-msg hook for conventional commits (optional)
echo "📝 Installing commit-msg hook..."
pre-commit install --hook-type commit-msg

# Run pre-commit on all files to ensure everything works
echo "🧪 Running pre-commit on all files to test setup..."
pre-commit run --all-files || {
    echo "⚠️  Some hooks failed. This is normal for the first run."
    echo "   The hooks have auto-fixed issues where possible."
    echo "   Please review the changes and commit them."
}

echo ""
echo "✅ Pre-commit setup complete!"
echo ""
echo "📋 What happens now:"
echo "   • Before each commit, the following will run automatically:"
echo "     - Black (code formatting)"
echo "     - isort (import sorting)"
echo "     - MyPy (type checking)"
echo "     - Flake8 (linting)"
echo "     - Bandit (security scanning)"
echo "     - LaTeX Formatter (for .tex files)"
echo "     - General checks (trailing whitespace, file endings, etc.)"
echo ""
echo "🔧 Manual commands:"
echo "   • Run hooks manually: pre-commit run --all-files"
echo "   • Update hooks: pre-commit autoupdate"
echo "   • Skip hooks: git commit --no-verify"
echo ""
echo "🎉 Happy coding!"
