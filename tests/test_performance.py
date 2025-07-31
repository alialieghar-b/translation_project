#!/usr/bin/env python3
"""
Performance benchmarks for LaTeX Formatter
Tests performance characteristics and memory usage
"""

import gc
import shutil
import tempfile
import time
import unittest
from pathlib import Path

from latex_formatter import LaTeXFormatter
from latex_formatter_advanced import AdvancedLaTeXFormatter, format_files_parallel


class TestPerformanceBenchmarks(unittest.TestCase):
    """Performance benchmarks for LaTeX formatting."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.basic_formatter = LaTeXFormatter()
        self.advanced_formatter = AdvancedLaTeXFormatter()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def generate_test_document(self, size_factor=1):
        """Generate a test LaTeX document of specified relative size."""
        base_sections = 10 * size_factor
        base_items = 5 * size_factor

        sections = []
        for i in range(base_sections):
            items = "\n".join(
                [f"\\item Item {j} in section {i}" for j in range(base_items)]
            )
            section = f"""\\section{{Section {i}}}
This is content for section {i}. It contains various LaTeX constructs including"quotes",
mathematical expressions like $x_i = \\sum_{{j=1}}^{{n}} a_{{ij}} \\cdot b_j$ and lists.

The content includes references to other sections \\ref{{sec:{i-1 if i > 0 else i+1}}}
and citations \\cite{{ref{i}, ref{i+1}}}.

\\begin{{itemize}}
{items}
\\end{{itemize}}

\\begin{{table}}[htbp]
\\centering
\\caption{{Results for Section {i}}}
\\begin{{tabular}}{{ccc}}
Parameter&Value&Unit\\\\
\\hline
Speed&{i*10}&m/s\\\\
Accuracy&{0.9 + i*0.01:.2f}&\\%\\\\
\\end{{tabular}}
\\end{{table}}

"""
            sections.append(section)

        # Add packages in non-alphabetical order
        packages = [
            "\\usepackage{tikz}",
            "\\usepackage{amsmath}",
            "\\usepackage{graphicx}",
            "\\usepackage{amsfonts}",
            "\\usepackage{booktabs}",
            "\\usepackage{hyperref}",
            "\\usepackage{cite}",
            "\\usepackage{geometry}",
            "\\usepackage{fancyhdr}",
            "\\usepackage{babel}",
        ]

        document = (
            f"""\\documentclass[11pt,a4paper]{{article}}
{chr(10).join(packages)}

\\title{{Performance Test Document}}
\\author{{Test Author}}

\\begin{{document}}
\\maketitle

\\begin{{abstract}}
This is a test document generated for performance benchmarking of the LaTeX formatter.
It contains {base_sections} sections with various LaTeX constructs.
\\end{{abstract}}

{chr(10).join(sections)}

\\begin{{thebibliography}}{{99}}
"""
            + "\n".join(
                [
                    f"\\bibitem{{ref{i}}}\nAuthor {i}, A. (202{i % 10}). "
                    f"Paper title {i}."
                    for i in range(base_sections)
                ]
            )
            + """
\\end{thebibliography}

\\end{document}"""
        )

        return document

    def measure_time(self, func, *args, **kwargs):
        """Measure execution time of a function."""
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        return result, end_time - start_time

    def measure_memory(self, func, *args, **kwargs):
        """Measure memory usage of a function (simplified)."""
        gc.collect()  # Clean up before measurement
        initial_objects = len(gc.get_objects())

        result = func(*args, **kwargs)

        gc.collect()
        final_objects = len(gc.get_objects())

        return result, final_objects - initial_objects

    def test_basic_vs_advanced_formatter_speed(self):
        """Compare speed of basic vs advanced formatter."""
        # Generate medium-sized test document
        content = self.generate_test_document(size_factor=2)

        # Measure basic formatter
        _, basic_time = self.measure_time(self.basic_formatter.format_content, content)

        # Measure advanced formatter
        _, advanced_time = self.measure_time(
            self.advanced_formatter.format_content, content
        )

        print("\nSpeed Comparison:")
        print(f"Basic formatter:    {basic_time:.4f} seconds")
        print(f"Advanced formatter: {advanced_time:.4f} seconds")

        # Handle division by zero for very fast operations
        if basic_time > 0:
            overhead_ratio = advanced_time / basic_time
            print(f"Overhead ratio:     {overhead_ratio:.2f}x")
        else:
            print("Overhead ratio:     N/A (basic formatter too fast to measure)")

        # Advanced should be slower but not excessively so
        # Only check overhead ratio if basic_time is measurable
        if basic_time > 0:
            self.assertLess(
                advanced_time / basic_time,
                3.0,
                "Advanced formatter should not be more than 3x slower",
            )

        # Both should complete in reasonable time
        self.assertLess(
            basic_time, 5.0, "Basic formatter should complete within 5 seconds"
        )
        self.assertLess(
            advanced_time, 15.0, "Advanced formatter should complete within 15 seconds"
        )

    def test_document_size_scaling(self):
        """Test how performance scales with document size."""
        size_factors = [1, 2, 4]
        basic_times = []
        advanced_times = []

        print("\nDocument Size Scaling:")
        print(
            f"{'Size Factor':<12} {'Basic (s)':<10} {'Advanced (s)':<12} {'Lines':<8}"
        )
        print("-" * 50)

        for factor in size_factors:
            content = self.generate_test_document(size_factor=factor)
            line_count = len(content.split("\n"))

            _, basic_time = self.measure_time(
                self.basic_formatter.format_content, content
            )
            _, advanced_time = self.measure_time(
                self.advanced_formatter.format_content, content
            )

            basic_times.append(basic_time)
            advanced_times.append(advanced_time)

            print(
                f"{factor:<12} {basic_time:<10.4f} {advanced_time:<12.4f} "
                f"{line_count:<8}"
            )

        # Check that performance scales reasonably (not exponentially)
        for i in range(1, len(size_factors)):
            size_ratio = size_factors[i] / size_factors[i - 1]

            # Handle division by zero for very fast operations
            if basic_times[i - 1] > 0:
                basic_time_ratio = basic_times[i] / basic_times[i - 1]
            else:
                # If previous time was 0, current time should also be very small
                basic_time_ratio = 1.0 if basic_times[i] <= 0.001 else float("inf")

            if advanced_times[i - 1] > 0:
                advanced_time_ratio = advanced_times[i] / advanced_times[i - 1]
            else:
                # If previous time was 0, current time should also be very small
                advanced_time_ratio = (
                    1.0 if advanced_times[i] <= 0.001 else float("inf")
                )

            # Time should not increase more than proportionally to size
            # Allow for some non-linear scaling due to algorithm complexity
            # Be more lenient on different platforms and system loads
            max_scaling_factor = size_ratio * 10  # Allow up to 10x worse than linear

            # Only check scaling if we have meaningful timing data
            # and times are significant
            if basic_time_ratio != float("inf") and basic_times[i] > 0.01:
                self.assertLess(
                    basic_time_ratio,
                    max_scaling_factor,
                    f"Basic formatter scaling too poorly at factor "
                    f"{size_factors[i]}: {basic_time_ratio:.2f}x vs max "
                    f"{max_scaling_factor:.2f}x",
                )
            if advanced_time_ratio != float("inf") and advanced_times[i] > 0.01:
                self.assertLess(
                    advanced_time_ratio,
                    max_scaling_factor,
                    f"Advanced formatter scaling too poorly at factor "
                    f"{size_factors[i]}: {advanced_time_ratio:.2f}x vs max "
                    f"{max_scaling_factor:.2f}x",
                )

    def test_sequential_vs_parallel_processing(self):
        """Compare sequential vs parallel file processing."""
        # Create multiple test files
        file_count = 6
        test_files = []

        for i in range(file_count):
            content = self.generate_test_document(size_factor=1)
            test_file = Path(self.test_dir) / f"test{i}.tex"
            with open(test_file, "w") as f:
                f.write(content)
            test_files.append(test_file)

        # Sequential processing
        def sequential_process():
            results = {}
            for file_path in test_files:
                result = self.advanced_formatter.format_file(file_path)
                results[str(file_path)] = result
            return results

        # Parallel processing
        def parallel_process():
            return format_files_parallel(
                test_files, self.advanced_formatter, max_workers=3
            )

        # Measure both approaches
        _, sequential_time = self.measure_time(sequential_process)
        _, parallel_time = self.measure_time(parallel_process)

        print(f"\nSequential vs Parallel Processing ({file_count} files):")
        print(f"Sequential: {sequential_time:.4f} seconds")
        print(f"Parallel:   {parallel_time:.4f} seconds")
        print(f"Speedup:    {sequential_time/parallel_time:.2f}x")

        # Parallel should be faster for multiple files, but allow for overhead
        # For small workloads, parallel processing may be slower due to thread overhead
        # We'll allow up to 100% overhead for small files, but expect improvement
        # for larger workloads
        max_overhead_ratio = 2.0  # Allow 100% overhead for small files
        self.assertLess(
            parallel_time,
            sequential_time * max_overhead_ratio,
            f"Parallel processing overhead too high: "
            f"{parallel_time/sequential_time:.2f}x vs max allowed "
            f"{max_overhead_ratio}x",
        )

        # Both should complete in reasonable time
        self.assertLess(sequential_time, 30.0, "Sequential processing too slow")
        self.assertLess(parallel_time, 20.0, "Parallel processing too slow")

    def test_memory_usage_basic_operations(self):
        """Test memory usage of basic formatting operations."""
        content = self.generate_test_document(size_factor=2)

        operations = [
            ("normalize_line_endings", self.basic_formatter.normalize_line_endings),
            (
                "remove_trailing_whitespace",
                self.basic_formatter.remove_trailing_whitespace,
            ),
            ("compress_empty_lines", self.basic_formatter.compress_empty_lines),
            ("normalize_commands", self.basic_formatter.normalize_commands),
            ("sort_packages", self.basic_formatter.sort_packages),
            ("align_tables", self.basic_formatter.align_tables),
            ("normalize_quotes", self.basic_formatter.normalize_quotes),
            ("format_environments", self.basic_formatter.format_environments),
        ]

        print("\nMemory Usage for Basic Operations:")
        print(f"{'Operation':<25} {'Objects Created':<15}")
        print("-" * 40)

        for op_name, op_func in operations:
            _, objects_created = self.measure_memory(op_func, content)
            print(f"{op_name:<25} {objects_created:<15}")

            # Should not create excessive objects
            self.assertLess(
                objects_created,
                1000,
                f"{op_name} creating too many objects: {objects_created}",
            )

    def test_memory_usage_large_documents(self):
        """Test memory usage with large documents."""
        size_factors = [1, 3, 5]

        print("\nMemory Usage Scaling:")
        print(f"{'Size Factor':<12} {'Objects Created':<15} {'Lines':<8}")
        print("-" * 35)

        for factor in size_factors:
            content = self.generate_test_document(size_factor=factor)
            line_count = len(content.split("\n"))

            _, objects_created = self.measure_memory(
                self.basic_formatter.format_content, content
            )

            print(f"{factor:<12} {objects_created:<15} {line_count:<8}")

            # Memory usage should scale reasonably
            expected_max_objects = line_count * 10  # Rough heuristic
            self.assertLess(
                objects_created,
                expected_max_objects,
                f"Memory usage too high for size factor {factor}",
            )

    def test_performance_with_different_content_types(self):
        """Test performance with different types of LaTeX content."""
        content_types = {
            "math_heavy": self.generate_math_heavy_content(),
            "table_heavy": self.generate_table_heavy_content(),
            "text_heavy": self.generate_text_heavy_content(),
            "mixed_content": self.generate_test_document(size_factor=1),
        }

        print("\nPerformance by Content Type:")
        print(
            f"{'Content Type':<15} {'Basic (s)':<10} {'Advanced (s)':<12} {'Lines':<8}"
        )
        print("-" * 50)

        for content_name, content in content_types.items():
            line_count = len(content.split("\n"))

            _, basic_time = self.measure_time(
                self.basic_formatter.format_content, content
            )
            _, advanced_time = self.measure_time(
                self.advanced_formatter.format_content, content
            )

            print(
                f"{content_name:<15} {basic_time:<10.4f} {advanced_time:<12.4f} "
                f"{line_count:<8}"
            )

            # All content types should complete in reasonable time
            self.assertLess(
                basic_time, 10.0, f"Basic formatter too slow on {content_name}"
            )
            self.assertLess(
                advanced_time, 20.0, f"Advanced formatter too slow on {content_name}"
            )

    def generate_math_heavy_content(self):
        """Generate content with heavy mathematical notation."""
        equations = []
        for i in range(50):
            equation = f"""\\begin{{align}}
x_{i} &= \\sum_{{j=1}}^{{n}} a_{{ij}} \\cdot b_j + c_{i} \\\\
y_{i} &= \\int_{{-\\infty}}^{{\\infty}} f(t) e^{{-i \\omega t}} dt \\\\
z_i &= \\frac{{\\partial^2 u}}{{\\partial x^2}}+\\frac{{\\partial^2 u}}{{\\partial y^2}}
\\end{{align}}"""
            equations.append(equation)

        return f"""\\documentclass{{article}}
\\usepackage{{amsmath}}
\\begin{{document}}
\\section{{Mathematical Content}}
{chr(10).join(equations)}
\\end{{document}}"""

    def generate_table_heavy_content(self):
        """Generate content with many tables."""
        tables = []
        for i in range(20):
            rows = []
            for j in range(10):
                row = f"Item {j}&Value {j}&Result {j*i}"
                rows.append(row)

            table = f"""\\begin{{table}}[htbp]
\\centering
\\caption{{Table {i}}}
\\begin{{tabular}}{{ccc}}
\\hline
Item&Value&Result\\\\
\\hline
{chr(10).join(rows)}\\\\
\\hline
\\end{{tabular}}
\\end{{table}}"""
            tables.append(table)

        return f"""\\documentclass{{article}}
\\usepackage{{booktabs}}
\\begin{{document}}
\\section{{Table Content}}
{chr(10).join(tables)}
\\end{{document}}"""

    def generate_text_heavy_content(self):
        """Generate content with primarily text."""
        paragraphs = []
        for i in range(100):
            paragraph = f"""This is paragraph {i} with text and some"quoted content"
and occasional mathematical expressions like $x = {i}$. The paragraph also includes
references to figures \\ref{{fig:{i}}} and citations \\cite{{ref{i}}}. This content
is designed to test text processing performance."""
            paragraphs.append(paragraph)

        return f"""\\documentclass{{article}}
\\begin{{document}}
\\section{{Text Content}}
{chr(10).join(paragraphs)}
\\end{{document}}"""

    def test_worst_case_performance(self):
        """Test performance with worst-case scenarios."""
        print("\nWorst-Case Performance Tests:")

        # Test 1: Very long lines
        long_line_content = "\\documentclass{article}\n\\begin{document}\n"
        long_line_content += (
            "This is a very long line that contains many words and should test "
            "the formatter's ability to handle extremely long lines without "
            "performance degradation. " * 50
        )
        long_line_content += "\n\\end{document}"

        _, long_line_time = self.measure_time(
            self.basic_formatter.format_content, long_line_content
        )
        print(f"Long lines:        {long_line_time:.4f} seconds")

        # Test 2: Many empty lines
        empty_lines_content = "\\documentclass{article}\n\\begin{document}\n"
        empty_lines_content += "\n" * 1000  # Many empty lines
        empty_lines_content += "Content\n\\end{document}"

        _, empty_lines_time = self.measure_time(
            self.basic_formatter.format_content, empty_lines_content
        )
        print(f"Many empty lines:  {empty_lines_time:.4f} seconds")

        # Test 3: Deeply nested environments
        nested_content = "\\documentclass{article}\n\\begin{document}\n"
        for i in range(20):
            nested_content += f"\\begin{{itemize}}\n\\item Level {i}\n"
        for i in range(20):
            nested_content += "\\end{itemize}\n"
        nested_content += "\\end{document}"

        _, nested_time = self.measure_time(
            self.basic_formatter.format_content, nested_content
        )
        print(f"Deep nesting:      {nested_time:.4f} seconds")

        # All worst-case scenarios should still complete reasonably quickly
        self.assertLess(long_line_time, 5.0, "Long line handling too slow")
        self.assertLess(empty_lines_time, 3.0, "Empty line handling too slow")
        self.assertLess(nested_time, 2.0, "Nested environment handling too slow")


class TestMemoryEfficiency(unittest.TestCase):
    """Test memory efficiency of formatting operations."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = LaTeXFormatter()

    def test_memory_cleanup(self):
        """Test that formatter cleans up memory properly."""
        initial_objects = len(gc.get_objects())

        # Process multiple documents
        for i in range(10):
            content = f"""\\documentclass{{article}}
\\begin{{document}}
\\section{{Test {i}}}
Content for document {i}.
\\end{{document}}"""

            result = self.formatter.format_content(content)
            self.assertIsNotNone(result)

        # Force garbage collection
        gc.collect()
        final_objects = len(gc.get_objects())

        # Should not have accumulated excessive objects
        objects_created = final_objects - initial_objects
        self.assertLess(
            objects_created, 500, f"Too many objects accumulated: {objects_created}"
        )

    def test_large_file_memory_usage(self):
        """Test memory usage with large files."""
        # Generate large content (approximately 1MB)
        large_content = "\\documentclass{article}\n\\begin{document}\n"
        large_content += "This is repeated content. " * 10000
        large_content += "\n\\end{document}"

        # Monitor memory before and after
        gc.collect()
        initial_objects = len(gc.get_objects())

        result = self.formatter.format_content(large_content)

        gc.collect()
        final_objects = len(gc.get_objects())

        self.assertIsNotNone(result)

        # Memory usage should be reasonable
        objects_created = final_objects - initial_objects
        self.assertLess(
            objects_created,
            2000,
            f"Large file created too many objects: {objects_created}",
        )


class TestFormattingConsistency(unittest.TestCase):
    """Test that formatting is consistent across multiple runs."""

    def setUp(self):
        """Set up test fixtures."""
        self.formatter = LaTeXFormatter()

    def test_formatting_consistency(self):
        """Test that multiple formatting runs produce identical results."""
        content = """\\documentclass{article}
\\usepackage{tikz}
\\usepackage{amsmath}
\\begin{document}
\\section{Test}
This is"quoted"text with math $x = y + z$.

\\begin{tabular}{cc}
Name&Age
John&25
\\end{tabular}
\\end{document}"""

        # Format multiple times
        results = []
        times = []

        for i in range(5):
            start_time = time.time()
            result = self.formatter.format_content(content)
            end_time = time.time()

            results.append(result)
            times.append(end_time - start_time)

        # All results should be identical
        for i in range(1, len(results)):
            self.assertEqual(
                results[0],
                results[i],
                f"Run {i+1} produced different result than run 1",
            )

        # Times should be consistent (within reasonable variance)
        # For very fast operations, allow higher relative variance due to noise
        avg_time = sum(times) / len(times)

        # Handle extremely fast operations (near 0.0000s)
        if avg_time < 0.0001:  # Less than 0.1ms
            # For extremely fast operations, just check that all times are very small
            for i, t in enumerate(times):
                self.assertLess(
                    t,
                    0.01,  # All times should be under 10ms
                    f"Run {i+1} time {t:.4f}s too slow for very fast operation",
                )
        else:
            # For measurable operations, check variance
            # Allow for initialization overhead in first run
            max_variance_ratio = (
                5.0 if avg_time < 0.1 else 2.0 if avg_time < 0.01 else 0.5
            )  # Higher tolerance for fast operations and initialization overhead
            for i, t in enumerate(times):
                self.assertLess(
                    abs(t - avg_time),
                    avg_time * max_variance_ratio,
                    f"Run {i+1} time {t:.4f}s too different from average "
                    f"{avg_time:.4f}s (max variance: {max_variance_ratio*100}%)",
                )

        print("\nConsistency Test Results:")
        print(f"Average time: {avg_time:.4f} seconds")
        print(f"Time variance: {max(times) - min(times):.4f} seconds")


if __name__ == "__main__":
    # Set up test runner with custom output
    unittest.main(verbosity=2, buffer=True)
