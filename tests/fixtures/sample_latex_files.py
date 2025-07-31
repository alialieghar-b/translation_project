#!/usr/bin/env python3
"""
Sample LaTeX content fixtures for testing
Provides various LaTeX document examples for comprehensive testing
"""

from typing import List, Optional

# Well-formed document samples
BASIC_ARTICLE = r"""
\documentclass{article}
\usepackage{amsmath}
\usepackage{graphicx}

\title{A Basic Article}
\author{Test Author}
\date{\today}

\begin{document}
\maketitle

\section{Introduction}
This is a basic LaTeX article with proper structure.

\section{Content}
Here is some content with mathematical expressions:
\begin{equation}
E = mc^2
\end{equation}

\subsection{Subsection}
More content here.

\end{document}
""".strip()

COMPLEX_DOCUMENT = r"""
\documentclass[11pt,a4paper]{report}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{hyperref}
\usepackage{natbib}
\usepackage{geometry}
\usepackage{fancyhdr}

\geometry{margin=1in}
\pagestyle{fancy}

\title{Complex Document Structure}
\author{John Doe \\ University of Example}
\date{December 2023}

\begin{document}
\maketitle
\tableofcontents

\chapter{Introduction}
This document demonstrates complex LaTeX features including citations~\cite{sample2023},
cross-references to Section~\ref{sec:methods}, and mathematical expressions.

\section{Background}
The field has evolved significantly. As shown in \citet{author2022}, the methodology
has improved dramatically.

\chapter{Methodology}
\label{sec:methods}
Our approach involves several steps:

\begin{enumerate}
\item Data collection from multiple sources
\item Statistical analysis using advanced techniques
\item Validation through cross-validation
\end{enumerate}

\section{Mathematical Framework}
The core equation governing our system is:

\begin{align}
\frac{\partial u}{\partial t} &= \nabla^2 u + f(x,y,t) \label{eq:pde} \\
u(x,y,0) &= u_0(x,y) \label{eq:initial} \\
\frac{\partial u}{\partial n}\bigg|_{\partial \Omega} &= g(x,y,t) \label{eq:boundary}
\end{align}

where $u(x,y,t)$ represents the solution field, and $f(x,y,t)$ is the source term.

\section{Results}
Table~\ref{tab:results} summarizes our findings.

\begin{table}[htbp]
\centering
\caption{Experimental Results}
\label{tab:results}
\begin{tabular}{@{}lccr@{}}
\toprule
Method & Accuracy (\%) & Time (s) & Memory (MB) \\
\midrule
Approach A & 94.5 & 12.3 & 256 \\
Approach B & 96.2 & 18.7 & 384 \\
Approach C & 91.8 & 8.9 & 192 \\
\bottomrule
\end{tabular}
\end{table}

\chapter{Discussion}
The results demonstrate the effectiveness of our approach. Figure~\ref{fig:comparison}
shows the performance comparison.

\begin{figure}[htbp]
\centering
\includegraphics[width=0.8\textwidth]{comparison.png}
\caption{Performance comparison of different approaches}
\label{fig:comparison}
\end{figure}

\chapter{Conclusion}
We have successfully demonstrated our methodology and achieved significant improvements
over existing approaches.

\bibliographystyle{plainnat}
\bibliography{references}

\appendix
\chapter{Additional Data}
Supplementary information is provided here.

\end{document}
""".strip()

# Malformed syntax examples
UNMATCHED_BRACES = r"""
\documentclass{article}
\begin{document}
\section{Test Section
Missing closing brace above.

\subsection{Another Section}
This has proper braces.

\section{Another Problem{
Extra opening brace here.
\end{document}
""".strip()

UNMATCHED_ENVIRONMENTS = r"""
\documentclass{article}
\begin{document}

\begin{itemize}
\item First item
\item Second item
% Missing \end{itemize}

\begin{enumerate}
\item Enumerated item
\end{enumerate}

\begin{center}
Centered text
% Missing \end{center}

\end{document}
""".strip()

INCOMPLETE_COMMANDS = r"""
\documentclass{article}
\begin{document}

\section{
\subsection
\item Without environment
\begin{itemize
\item Incomplete begin

\textbf{Bold text
\emph{Emphasized

\end{document}
""".strip()

# Complex table structures
COMPLEX_TABLES = r"""
\documentclass{article}
\usepackage{booktabs}
\usepackage{array}
\usepackage{multirow}

\begin{document}

\section{Table Examples}

\subsection{Basic Table}
\begin{table}[htbp]
\centering
\caption{Basic table}
\begin{tabular}{lcc}
\toprule
Name & Age & City \\
\midrule
John & 25 & New York \\
Jane & 30 & Los Angeles \\
Bob & 35 & Chicago \\
\bottomrule
\end{tabular}
\end{table}

\subsection{Complex Table with Multirow and Multicolumn}
\begin{table}[htbp]
\centering
\caption{Complex table structure}
\begin{tabular}{|l|c|c|c|c|}
\hline
\multirow{2}{*}{Category} & \multicolumn{2}{c|}{Group A} & \\
    \multicolumn{2}{c|}{Group B} \\
\cline{2-5}
& Value 1 & Value 2 & Value 3 & Value 4 \\
\hline
Type X & 12.5 & 15.8 & 18.2 & 20.1 \\
Type Y & 8.9 & 11.3 & 14.7 & 17.6 \\
Type Z & 20.1 & 22.4 & 25.8 & 28.3 \\
\hline
\end{tabular}
\end{table}

\subsection{Table with Mathematical Content}
\begin{table}[htbp]
\centering
\caption{Mathematical expressions in tables}
\begin{tabular}{ccc}
\toprule
Function & Derivative & Integral \\
\midrule
$x^2$ & $2x$ & $\frac{x^3}{3}$ \\
$\sin(x)$ & $\cos(x)$ & $-\cos(x)$ \\
$e^x$ & $e^x$ & $e^x$ \\
$\ln(x)$ & $\frac{1}{x}$ & $x\ln(x) - x$ \\
\bottomrule
\end{tabular}
\end{table}

\subsection{Misaligned Table}
\begin{tabular}{ccc}
Name&Age&Very Long City Name
John&25&NYC
Jane&30&Los Angeles
Bob&35&Chicago
\end{tabular}

\end{document}
""".strip()

# Mathematical expressions
COMPLEX_MATH = r"""
\documentclass{article}
\usepackage{amsmath,amssymb,amsthm}

\begin{document}

\section{Mathematical Examples}

\subsection{Basic Equations}
Inline math: $x^2 + y^2 = z^2$ and display math:
\[
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
\]

\subsection{Alignment Environments}
\begin{align}
f(x) &= \sum_{n=0}^{\infty} \frac{f^{(n)}(a)}{n!}(x-a)^n \\
&= f(a) + f'(a)(x-a) + \frac{f''(a)}{2!}(x-a)^2 + \cdots \\
&= \lim_{n \to \infty} \sum_{k=0}^{n} \frac{f^{(k)}(a)}{k!}(x-a)^k
\end{align}

\subsection{Matrix Operations}
\begin{equation}
\mathbf{A} = \begin{pmatrix}
a_{11} & a_{12} & \cdots & a_{1n} \\
a_{21} & a_{22} & \cdots & a_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
a_{m1} & a_{m2} & \cdots & a_{mn}
\end{pmatrix}
\end{equation}

\subsection{Complex Fractions}
\begin{equation}
\frac{\frac{a+b}{c+d}}{\frac{e+f}{g+h}} = \frac{(a+b)(g+h)}{(c+d)(e+f)}
\end{equation}

Continued fraction:
\begin{equation}
\pi = 3 + \cfrac{1}{7 + \cfrac{1}{15 + \cfrac{1}{1 + \cfrac{1}{292 + \cdots}}}}
\end{equation}

\subsection{Cases and Piecewise Functions}
\begin{equation}
f(x) = \begin{cases}
x^2 & \text{if } x \geq 0 \\
-x^2 & \text{if } x < 0
\end{cases}
\end{equation}

\subsection{Integrals and Summations}
\begin{align}
\sum_{n=1}^{\infty} \frac{1}{n^2} &= \frac{\pi^2}{6} \\
\int_0^1 \int_0^1 \frac{x-y}{(x+y)^3} \, dx \, dy &= 0 \\
\oint_C \mathbf{F} \cdot d\mathbf{r} &= \\
    \iint_S (\nabla \times \mathbf{F}) \cdot \mathbf{n} \, dS
\end{align}

\end{document}
""".strip()

# Bibliography examples
BIBLIOGRAPHY_EXAMPLES = r"""
\documentclass{article}
\usepackage{natbib}

\begin{document}

\section{Citations}
See \cite{knuth1984texbook} for more information about \TeX.
According to \citet{lamport1994latex}, \LaTeX{} is a document preparation system.
Multiple citations: \citep{knuth1984texbook,lamport1994latex,mittelbach2004latex}.

\section{Different Citation Styles}
\citeauthor{knuth1984texbook} wrote about typesetting.
The work was published in \citeyear{lamport1994latex}.
For page references: \citep[p.~25]{knuth1984texbook}.

\bibliographystyle{plainnat}

\begin{thebibliography}{99}

\bibitem[Knuth(1984)]{knuth1984texbook}
Knuth, D.~E.
\newblock {\em The \TeX book}.
\newblock Addison-Wesley, Reading, Massachusetts, 1984.

\bibitem[Lamport(1994)]{lamport1994latex}
Lamport, L.
\newblock {\em \LaTeX: A Document Preparation System}.
\newblock Addison-Wesley, Reading, Massachusetts, second edition, 1994.

\bibitem[Mittelbach et~al.(2004)]{mittelbach2004latex}
Mittelbach, F., Goossens, M., Braams, J., Carlisle, D., and Rowley, C.
\newblock {\em The \LaTeX Companion}.
\newblock Addison-Wesley, Boston, second edition, 2004.

\bibitem[Gratzer(2007)]{gratzer2007more}
Gr\"atzer, G.
\newblock {\em More Math Into \LaTeX}.
\newblock Springer, New York, fourth edition, 2007.

\end{thebibliography}

\end{document}
""".strip()

# Encoding test content
UTF8_CONTENT = r"""
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}

\begin{document}

\section{UTF-8 Character Examples}

\subsection{European Languages}
\begin{itemize}
\item English: Hello, world!
\item French: Bonjour le monde! Café, naïve, résumé
\item German: Hallo Welt! Ä, Ö, Ü, ß
\item Spanish: ¡Hola mundo! Niño, señorita
\item Italian: Ciao mondo! Città, più
\item Portuguese: Olá mundo! São, coração
\end{itemize}

\subsection{Mathematical Symbols}
Greek letters: α, β, γ, δ, ε, ζ, η, θ, ι, κ, λ, μ, ν, ξ, ο, π, ρ, σ, τ, υ, φ, χ, ψ, ω
Mathematical operators: ∀, ∃, ∈, ∉, ∪, ∩, ⊂, ⊃, ∅, ∞, ≤, ≥, ≠, ≈, ±, ×, ÷
Arrows: →, ←, ↑, ↓, ↔, ⇒, ⇐, ⇔

\subsection{Currency and Symbols}
Currencies: €, £, ¥, $, ¢, ₹
Other symbols: ©, ®, ™, §, ¶, †, ‡, •, …

\subsection{Non-Latin Scripts}
\begin{itemize}
\item Russian: Привет мир! Москва
\item Chinese: 你好世界！北京
\item Japanese: こんにちは世界！東京
\item Arabic: مرحبا بالعالم
\item Hebrew: שלום עולם
\end{itemize}

\end{document}
""".strip()


# Performance test content generator
def get_sample_content(name: str) -> str:
    """Get sample content by name - moved to after SAMPLE_DOCUMENTS definition."""
    return SAMPLE_DOCUMENTS.get(name, "")


def get_all_sample_names() -> List[str]:
    """Get list of all available sample names - moved to after
    SAMPLE_DOCUMENTS definition."""
    return list(SAMPLE_DOCUMENTS.keys())


def create_test_file(name: str, content: Optional[str] = None) -> str:
    """Create a temporary test file with given content."""
    import tempfile

    if content is None:
        content = get_sample_content(name)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False) as f:
        f.write(content)
        return f.name


def generate_large_document(sections: int = 100, items_per_section: int = 10) -> str:
    """Generate a large document for performance testing."""
    header = r"""
\documentclass{article}
\usepackage{amsmath}
\usepackage{graphicx}
\usepackage{booktabs}

\title{Large Document for Performance Testing}
\author{Test Generator}

\begin{document}
\maketitle
\tableofcontents
""".strip()

    sections_content = []
    for i in range(sections):
        items = []
        for j in range(items_per_section):
            items.append(
                f"\\item Item {j+1} in section {i+1} with some mathematical "
                f"content: $x_{{i+1}} = \\sum_{{k=1}}^{{{j+1}}} a_k$"
            )

        section = f"""
\\section{{Section {i+1}}}
This is section {i+1} with various LaTeX constructs. It contains"quoted text"
and mathematical expressions like $f(x) = x^2 + {i}x + {j}$.

\\begin{{itemize}}
{chr(10).join(items)}
\\end{{itemize}}

\\begin{{table}}[htbp]
\\centering
\\caption{{Table for Section {i+1}}}
\\begin{{tabular}}{{ccc}}
\\toprule
Parameter & Value & Unit \\\\
\\midrule
Speed & {i*10} & m/s \\\\
Accuracy & {90 + i*0.1:.1f} & \\% \\\\
\\bottomrule
\\end{{tabular}}
\\end{{table}}
"""
        sections_content.append(section)

    footer = r"""
\end{document}
""".strip()

    return header + "\n\n" + "\n".join(sections_content) + "\n\n" + footer


# Stress test content
STRESS_TEST_CONTENT = {
    "deeply_nested": r"""
\documentclass{article}
\begin{document}
"""
    + "\n".join(f"\\begin{{itemize}}\n\\item Level {i}" for i in range(50))
    + "\n"
    + "\n".join("\\end{itemize}" for _ in range(50))
    + r"""
\end{document}
""",
    "very_long_line": r"""
\documentclass{article}
\begin{document}
"""
    + (
        "This is a very long line that contains many repeated words and "
        "phrases to test the formatter's ability to handle extremely long "
        "lines without performance degradation or memory issues. "
    )
    * 100
    + r"""
\end{document}
""",
    "many_empty_lines": r"""
\documentclass{article}
\begin{document}
Content before empty lines.
"""
    + "\n" * 1000
    + r"""
Content after empty lines.
\end{document}
""",
}

# Real-world document examples
THESIS_TEMPLATE = r"""
\documentclass[12pt,oneside]{book}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{hyperref}
\usepackage{natbib}
\usepackage{geometry}
\usepackage{fancyhdr}
\usepackage{setspace}

\geometry{letterpaper,margin=1in}
\doublespacing
\pagestyle{fancy}

\newtheorem{theorem}{Theorem}[chapter]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{corollary}[theorem]{Corollary}

\title{A Comprehensive Study of Advanced Topics}
\author{Graduate Student}
\date{2023}

\begin{document}

\frontmatter
\maketitle

\begin{abstract}
This thesis presents a comprehensive study of advanced topics in the field.
We investigate several key areas and provide novel contributions to the literature.
The work demonstrates significant improvements over existing methodologies.
\end{abstract}

\tableofcontents
\listoffigures
\listoftables

\mainmatter

\chapter{Introduction}
\label{chap:intro}

The field of study has evolved significantly over the past decades. This thesis
contributes to the understanding of complex systems through both theoretical
analysis and empirical validation.

\section{Motivation}
The motivation for this work stems from several key observations:
\begin{enumerate}
\item Existing methods have limitations in handling complex scenarios
\item There is a need for more robust theoretical frameworks
\item Practical applications require improved efficiency
\end{enumerate}

\section{Contributions}
The main contributions of this thesis are:
\begin{itemize}
\item Development of a novel theoretical framework
\item Empirical validation through extensive experiments
\item Practical applications demonstrating real-world utility
\end{itemize}

\chapter{Literature Review}
\label{chap:literature}

This chapter provides a comprehensive review of existing literature.

\section{Historical Development}
The field began with the seminal work of \citet{pioneer1950} who first
introduced the fundamental concepts.

\section{Recent Advances}
Recent developments have focused on improving efficiency and robustness
\citep{recent2020,another2021}.

\chapter{Methodology}
\label{chap:methodology}

Our approach combines theoretical analysis with empirical validation.

\section{Theoretical Framework}
We develop a comprehensive theoretical framework based on the following principles:

\begin{theorem}
\label{thm:main}
For any system satisfying conditions A, B, and C, there exists a unique
solution to the optimization problem.
\end{theorem}

\begin{proof}
The proof follows from the application of standard optimization theory
combined with our novel constraints.
\end{proof}

\chapter{Results}
\label{chap:results}

This chapter presents the main results of our investigation.

\section{Experimental Setup}
We conducted extensive experiments using the following setup:
\begin{itemize}
\item Hardware: High-performance computing cluster
\item Software: Custom implementation in Python and C++
\item Datasets: Standard benchmarks plus novel synthetic data
\end{itemize}

\section{Performance Analysis}
Table~\ref{tab:performance} shows the performance comparison.

\begin{table}[htbp]
\centering
\caption{Performance comparison with existing methods}
\label{tab:performance}
\begin{tabular}{@{}lccr@{}}
\toprule
Method & Accuracy (\%) & Time (s) & Memory (GB) \\
\midrule
Baseline & 85.2 & 120.5 & 2.1 \\
Improved & 92.7 & 95.3 & 1.8 \\
Our Method & 96.4 & 78.2 & 1.5 \\
\bottomrule
\end{tabular}
\end{table}

\chapter{Discussion}
\label{chap:discussion}

The results demonstrate the effectiveness of our approach across multiple
dimensions.

\chapter{Conclusion}
\label{chap:conclusion}

This thesis has presented a comprehensive study of advanced topics with
significant contributions to both theory and practice.

\section{Future Work}
Several directions for future research emerge from this work:
\begin{itemize}
\item Extension to more complex scenarios
\item Investigation of alternative optimization strategies
\item Development of more efficient implementations
\end{itemize}

\backmatter
\bibliographystyle{plainnat}
\bibliography{references}

\appendix
\chapter{Additional Proofs}
Detailed proofs of supporting lemmas are provided here.

\chapter{Implementation Details}
Technical implementation details are documented in this appendix.

\end{document}
""".strip()

# Export all content for easy import
SAMPLE_DOCUMENTS = {
    "basic_article": BASIC_ARTICLE,
    "complex_document": COMPLEX_DOCUMENT,
    "unmatched_braces": UNMATCHED_BRACES,
    "unmatched_environments": UNMATCHED_ENVIRONMENTS,
    "incomplete_commands": INCOMPLETE_COMMANDS,
    "complex_tables": COMPLEX_TABLES,
    "complex_math": COMPLEX_MATH,
    "bibliography_examples": BIBLIOGRAPHY_EXAMPLES,
    "utf8_content": UTF8_CONTENT,
    "thesis_template": THESIS_TEMPLATE,
}


# Performance test content generator (moved to after dictionary definition)
# Note: These functions are duplicates and should be removed


if __name__ == "__main__":
    # Demonstration of available samples
    print("Available LaTeX sample documents:")
    for name, content in SAMPLE_DOCUMENTS.items():
        lines = len(content.split("\n"))
        chars = len(content)
        print(f"  {name}: {lines} lines, {chars} characters")

    print(f"\nStress test content types: {list(STRESS_TEST_CONTENT.keys())}")
    print("Use generate_large_document(sections, items) for performance testing")
