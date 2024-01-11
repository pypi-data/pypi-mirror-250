"""Unit tests for an ns2json module.

"""

import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from src.ns2json.dns import type_a, type_aaaa, type_mx, type_ns, type_soa, type_txt, clean_raw_data  # pylint: disable=C0413


class TestNS2JSON(unittest.TestCase):
    """Unit tests for an types function.

    """

    def test_type_a(self):
        """A test for type A clean and format data.

        """

        output = [
        """
        Server:  one.one.one.one
        Address:  1.1.1.1

        Non-authoritative answer:
        Name:    pypi.org
        Addresses:  151.101.192.223
                151.101.0.223
                151.101.64.223
                151.101.128.223
        """,
        """
        Server:  one.one.one.one
        Address:  1.1.1.1

        Non-authoritative answer:
        Name:    google.com
        Address:  216.58.215.110
        """
        ]
        result = [
            ['151.101.192.223', '151.101.0.223', '151.101.64.223', '151.101.128.223'],
            ['216.58.215.110']
        ]
        dns_resolver = '1.1.1.1'

        for i in range(2):
            clean_data = clean_raw_data.clean_stdout(output[i])
            self.assertEqual(type_a.extract_type_a(clean_data, dns_resolver), result[i])
    

    def test_type_aaaa(self):
        """A test for type AAAA clean and format data.

        """

        output = [
        """
        Server:  one.one.one.one
        Address:  1.1.1.1

        Non-authoritative answer:
        Name:    google.com
        Address:  2a00:1450:401b:808::200e
        """,
        """
        Server:  one.one.one.one
        Address:  1.1.1.1

        Non-authoritative answer:
        Name:    cloudflare.com
        Addresses:  2606:4700::6810:85e5
          2606:4700::6810:84e5
        """
        ]
        result = [
            ['2a00:1450:401b:808::200e'],
            ['2606:4700::6810:85e5', '2606:4700::6810:84e5']
        ]
        dns_resolver = '1.1.1.1'

        for i in range(2):
            clean_data = clean_raw_data.clean_stdout(output[i])
            self.assertEqual(type_aaaa.extract_type_aaaa(clean_data, dns_resolver), result[i])


    def test_type_mx(self):
        """A test for type MX clean and format data.

        """

        output = [
        """
        Server:  one.one.one.one
        Address:  1.1.1.1

        Non-authoritative answer:
        google.com      MX preference = 10, mail exchanger = smtp.google.com
        """,
        """
        Server:  one.one.one.one
        Address:  1.1.1.1

        Non-authoritative answer:
        cloudflare.com  MX preference = 5, mail exchanger = mailstream-canary.mxrecord.io
        cloudflare.com  MX preference = 10, mail exchanger = mailstream-east.mxrecord.io
        cloudflare.com  MX preference = 10, mail exchanger = mailstream-west.mxrecord.io
        cloudflare.com  MX preference = 20, mail exchanger = mailstream-central.mxrecord.mx
        """
        ]
        result = [
            [['10', 'smtp.google.com']],
            [['5', 'mailstream-canary.mxrecord.io'], ['10', 'mailstream-east.mxrecord.io'], ['10', 'mailstream-west.mxrecord.io'], ['20', 'mailstream-central.mxrecord.mx']]
        ]
        addresses = ['google.com', 'cloudflare.com']

        for i in range(2):
            clean_data = clean_raw_data.clean_stdout(output[i])
            self.assertEqual(type_mx.extract_type_mx(clean_data, addresses[i]), result[i])
    

    def test_type_ns(self):
        """A test for type NS clean and format data.

        """

        output = [
        """
        Server:  one.one.one.one
        Address:  1.1.1.1

        Non-authoritative answer:
        google.com      nameserver = ns4.google.com
        google.com      nameserver = ns3.google.com
        google.com      nameserver = ns2.google.com
        google.com      nameserver = ns1.google.com
        """,
        """
        Server:  one.one.one.one
        Address:  1.1.1.1

        Non-authoritative answer:
        cloudflare.com  nameserver = ns3.cloudflare.com
        cloudflare.com  nameserver = ns4.cloudflare.com
        cloudflare.com  nameserver = ns5.cloudflare.com
        cloudflare.com  nameserver = ns6.cloudflare.com
        cloudflare.com  nameserver = ns7.cloudflare.com
        """]
        result = [
            ['ns4.google.com', 'ns3.google.com', 'ns2.google.com', 'ns1.google.com'],
            ['ns3.cloudflare.com', 'ns4.cloudflare.com', 'ns5.cloudflare.com', 'ns6.cloudflare.com', 'ns7.cloudflare.com',]
        ]
        addresses = ['google.com', 'cloudflare.com']

        for i in range(2):
            clean_data = clean_raw_data.clean_stdout(output[i])
            self.assertEqual(type_ns.extract_type_ns(clean_data, addresses[i]), result[i])


    def test_type_soa(self):
        """A test for type SOA clean and format data.

        """

        output = [
        """
        Server:  one.one.one.one
        Address:  1.1.1.1

        Non-authoritative answer:
        google.com
                primary name server = ns1.google.com
                responsible mail addr = dns-admin.google.com
                serial  = 596875701
                refresh = 900 (15 mins)
                retry   = 900 (15 mins)
                expire  = 1800 (30 mins)
                default TTL = 60 (1 min)
        """,
        """
        Server:  one.one.one.one
        Address:  1.1.1.1

        Non-authoritative answer:
        cloudflare.com
        primary name server = ns3.cloudflare.com
        responsible mail addr = dns.cloudflare.com
        serial  = 2330392126
        refresh = 10000 (2 hours 46 mins 40 secs)
        retry   = 2400 (40 mins)
        expire  = 604800 (7 days)
        default TTL = 300 (5 mins)
        """]
        result = [
            [['primarynameserver', 'ns1.google.com'], ['responsiblemailaddr', 'dns-admin.google.com'], ['serial', '596875701'], ['refresh', '900'], ['retry', '900'], ['expire', '1800'], ['defaultTTL', '60']],
            [['primarynameserver', 'ns3.cloudflare.com'], ['responsiblemailaddr', 'dns.cloudflare.com'], ['serial', '2330392126'], ['refresh', '10000'], ['retry', '2400'], ['expire', '604800'], ['defaultTTL', '300']]
        ]

        for i in range(2):
            clean_data = clean_raw_data.clean_stdout(output[i])
            self.assertEqual(type_soa.extract_type_soa(clean_data), result[i])
        

    def test_type_txt(self):
        """A test for type TXT clean and format data.

        """

        output = [
        """
        Server:  one.one.one.one
        Address:  1.1.1.1

        Non-authoritative answer:
        pypi.org        text =

        "google-site-verification=YdrllWIiutXFzqhEamHP4HgCoh88dTFzb2A6QFljooc"
        pypi.org        text =

        "google-site-verification=ZI8zeHE6SWuJljW3f4csGetjOWo4krvjf13tdORsH4Y"
        pypi.org        text =

        "v=spf1 include:_spf.google.com include:amazonses.com include:helpscoutemail.com -all"
        """,
        """
        Server:  one.one.one.one
        Address:  1.1.1.1

        Non-authoritative answer:
        realpython.com  text =

        "facebook-domain-verification=mq46mq2is4d14vhplara08baid717h"
        realpython.com  text =

        "google-site-verification=A7KGy9dXNDDjfcJxzeheQMV3zXmEaGyhfXGD8gVnV0o"
        realpython.com  text =

        "google-site-verification=Ubborzk4tBqoxnQn8nPqAyMvR6MFiJEJABBL8_y63QQ"
        realpython.com  text =

        "heroku-domain-verification=4wmxxfa6kei5mnhcv1uv9tupeqkktlelsdph/9h1zyw"
        realpython.com  text =

        "v=spf1 include:sendgrid.net include:_spf.google.com include:spf.mtasv.net -all"
        realpython.com  text =

        "ahrefs-site-verification_b23bde4d9aec7044956dcd71cf0d11f916b0e454decab322485d1711448974f4"
        """]
        result = [
            ["google-site-verification=YdrllWIiutXFzqhEamHP4HgCoh88dTFzb2A6QFljooc", "google-site-verification=ZI8zeHE6SWuJljW3f4csGetjOWo4krvjf13tdORsH4Y", "v=spf1 include:_spf.google.com include:amazonses.com include:helpscoutemail.com -all"],
            ["facebook-domain-verification=mq46mq2is4d14vhplara08baid717h", "google-site-verification=A7KGy9dXNDDjfcJxzeheQMV3zXmEaGyhfXGD8gVnV0o", "google-site-verification=Ubborzk4tBqoxnQn8nPqAyMvR6MFiJEJABBL8_y63QQ", "heroku-domain-verification=4wmxxfa6kei5mnhcv1uv9tupeqkktlelsdph/9h1zyw", "v=spf1 include:sendgrid.net include:_spf.google.com include:spf.mtasv.net -all", "ahrefs-site-verification_b23bde4d9aec7044956dcd71cf0d11f916b0e454decab322485d1711448974f4"]
        ]
        addresses = ['pypi.org', 'realpython.com']

        for i in range(2):
            clean_data = clean_raw_data.clean_stdout_for_type_txt(output[i], addresses[i])
            self.assertEqual(type_txt.extract_type_txt(clean_data), result[i])


if __name__ == "__main__":
    unittest.main()
