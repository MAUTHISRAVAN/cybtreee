import argparse
import json
from datetime import datetime
from modules.domain_reader import DomainReader
from modules.scanner import Scanner
from modules.risk_analyzer import RiskAnalyzer
from modules.report_generator import ReportGenerator

def main():
    parser = argparse.ArgumentParser(description='Attack Surface Monitoring Tool')
    parser.add_argument('-i', '--input', required=True, help='Input CSV file containing domains')
    parser.add_argument('-o', '--output', default='reports', help='Output directory for reports')
    parser.add_argument('--format', choices=['json', 'markdown', 'html'], default='json',
                       help='Output format (default: json)')
    args = parser.parse_args()

    # Initialize components
    domain_reader = DomainReader(args.input)
    scanner = Scanner()
    risk_analyzer = RiskAnalyzer()
    report_generator = ReportGenerator(args.output)

    # Process each domain
    for domain in domain_reader.get_domains():
        print(f"\nScanning domain: {domain}")
        
        # Perform scanning
        scan_results = scanner.scan_domain(domain)
        
        # Analyze risks
        risk_analysis = risk_analyzer.analyze(scan_results)
        
        # Generate report
        report = {
            "domain": domain,
            "scan_date": datetime.now().strftime("%Y-%m-%d"),
            "risk_score": risk_analysis["risk_score"],
            "risk_summary": risk_analysis["summary"],
            **scan_results
        }
        
        # Save report
        report_generator.generate(report, args.format)

if __name__ == "__main__":
    main()
