import nslookup
from dns import resolver
import dns.reversename

#print("load " + '/'.join(__file__.split('/')[-2:]))

class Nslookup():
    def __init__(self, server:list[str]=["8.8.8.8", "1.1.1.1", "8.8.4.4"], tcp:bool=False) -> None:
        self.nslookup = nslookup.Nslookup(dns_servers=server, tcp=tcp)
        self.resolver = resolver.Resolver()
        self.resolver.nameservers = server
    
    def A(self, domain:str) -> list[str]:
        return self.nslookup.dns_lookup(domain).answer
    
    def AAAA(self, domain:str) -> list[str]:
        return self.nslookup.dns_lookup6(domain).answer
    
    def Reverse(self, ip:str) -> str:
        return str(self.resolver.resolve(dns.reversename.from_address(ip), "PTR")[0])
    
    