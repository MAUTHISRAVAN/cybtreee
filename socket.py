import subprocess
import socket
import dns.resolver
import requests
from typing import Dict, Any

class Scanner:
    def __init__(self):
        self.tools = self._check_required_tools()

    def _check_required_tools(self) -> Dict[str, bool]:
        tools = {
            'nmap': self._is_tool_installed('nmap'),
            'amass': self._is_tool_installed('amass'),
            'subfinder': self._is_tool_installed('subfinder')
        }
        return tools

    def _is_tool_installed(self, tool_name: str) -> bool:
        try:
            subprocess.run([tool_name, '--version'], 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
            return True
        except FileNotFoundError:
            return False

    def scan_domain(self, domain: str) -> Dict[str, Any]:
        results = {
            "subdomains": self._enumerate_subdomains(domain),
            "dns_records": self._get_dns_records(domain),
            "open_ports": self._scan_ports(domain),
            "tech_stack": self._detect_tech_stack(domain),
            "headers": self._check_headers(domain),
            "ssl_info": self._check_ssl(domain),
            "sensitive_paths": self._discover_paths(domain)
        }
        return results

    # Implement individual scanning methods here
    def _enumerate_subdomains(self, domain: str) -> List[str]:
        # Implementation for subdomain enumeration
        pass

    def _get_dns_records(self, domain: str) -> Dict[str, Any]:
        # Implementation for DNS records
        pass

    # Add other scanning methods...
    
    def _enumerate_subdomains(self, domain: str) -> List[str]:
    subdomains = set()
    
    # Using subfinder if available
    if self.tools['subfinder']:
        try:
            result = subprocess.run(['subfinder', '-d', domain], 
                                  capture_output=True, text=True)
            subdomains.update(result.stdout.strip().split('\n'))
        except Exception as e:
            print(f"Subfinder error: {str(e)}")

    # Using amass if available
    if self.tools['amass']:
        try:
            result = subprocess.run(['amass', 'enum', '-d', domain],
                                  capture_output=True, text=True)
            subdomains.update(result.stdout.strip().split('\n'))
        except Exception as e:
            print(f"Amass error: {str(e)}")

    # Filter out empty strings and verify subdomains are alive
    verified_subdomains = []
    for subdomain in subdomains:
        if subdomain and self._is_subdomain_alive(subdomain):
            verified_subdomains.append(subdomain)

    return verified_subdomains

def _is_subdomain_alive(self, subdomain: str) -> bool:
    try:
        response = requests.get(f"https://{subdomain}", 
                              timeout=5, 
                              verify=False)
        return response.status_code < 500
    except:
        try:
            response = requests.get(f"http://{subdomain}", 
                                  timeout=5)
            return response.status_code < 500
        except:
            return False

def _get_dns_records(self, domain: str) -> Dict[str, Any]:
    dns_records = {}
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA']
    
    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            dns_records[record_type] = [str(answer) for answer in answers]
        except Exception as e:
            dns_records[record_type] = []
    
    # Get WHOIS information
    try:
        import whois
        whois_info = whois.whois(domain)
        dns_records['WHOIS'] = {
            'registrar': whois_info.registrar,
            'creation_date': str(whois_info.creation_date),
            'expiration_date': str(whois_info.expiration_date),
            'name_servers': whois_info.name_servers
        }
    except Exception as e:
        dns_records['WHOIS'] = {'error': str(e)}

    return dns_records
    def _scan_ports(self, domain: str) -> List[Dict[str, Any]]:
    if not self.tools['nmap']:
        return [{'error': 'nmap not installed'}]
    
    try:
        # Resolve domain to IP
        ip = socket.gethostbyname(domain)
        
        # Run nmap scan
        result = subprocess.run(
            ['nmap', '-sV', '-T4', '-p-', '--open', ip],
            capture_output=True,
            text=True
        )
        
        # Parse nmap output
        ports = []
        current_port = None
