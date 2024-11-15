from typing import Self
from typing import Optional
from cryptography.hazmat.primitives.serialization import pkcs12

import pydantic


__all__ = [
    "CertificateInfo",
    "debug_certificate_info",
]


class CertificateInfo(pydantic.BaseModel):
    signer_name: str = pydantic.Field(..., validation_alias="commonName")

    @classmethod
    def parse(cls, pfx_data: bytes, passphrase: Optional[bytes] = None) -> Self:
        private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
            data=pfx_data,
            password=passphrase
        )
        assert certificate

        info = {}

        for attr in certificate.subject:
            k = attr.oid._name
            if k in ["commonName"]:
                info[k] = attr.value

        return cls(**info)


def debug_certificate_info(pfx_data: bytes, passphrase: Optional[bytes] = None) -> None:
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes

    private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
        data=pfx_data,
        password=passphrase
    )

    if certificate:
        print("Certificate Details:")
        print("-" * 20)

        # Subject Information
        print("Subject:")
        for attr in certificate.subject:
            print(f"  {attr.oid._name}: {attr.value}")

        # Issuer Information
        print("\nIssuer:")
        for attr in certificate.issuer:
            print(f"  {attr.oid._name}: {attr.value}")

        # Validity Period
        print(f"\nValid From: {certificate.not_valid_before_utc}")
        print(f"Valid Until: {certificate.not_valid_after_utc}")

        # Serial Number
        print(f"\nSerial Number: {certificate.serial_number}")

        # Version
        print(f"Version: {certificate.version}")

        # Signature Algorithm
        print(f"Signature Algorithm: {certificate.signature_algorithm_oid._name}")

        # Public Key
        public_key = certificate.public_key()
        print(f"\nPublic Key Type: {type(public_key).__name__}")
        print(f"Public Key Size: {public_key.key_size} bits")

        # Extensions
        print("\nExtensions:")
        for extension in certificate.extensions:
            print(f"  {extension.oid._name}:")
            if isinstance(extension.value, x509.BasicConstraints):
                print(f"    CA: {extension.value.ca}")
                print(f"    Path Length: {extension.value.path_length}")
            elif isinstance(extension.value, x509.SubjectAlternativeName):
                print("    Subject Alternative Names:")
                for name in extension.value:
                    print(f"      {name}")
            elif isinstance(extension.value, x509.KeyUsage):
                print(f"    Digital Signature: {extension.value.digital_signature}")
                print(f"    Content Commitment: {extension.value.content_commitment}")
                print(f"    Key Encipherment: {extension.value.key_encipherment}")
                print(f"    Data Encipherment: {extension.value.data_encipherment}")
                print(f"    Key Agreement: {extension.value.key_agreement}")
                print(f"    Certificate Sign: {extension.value.key_cert_sign}")
                print(f"    CRL Sign: {extension.value.crl_sign}")
            else:
                print(f"    {extension.value}")

        # Fingerprints
        print("\nFingerprints:")
        for algorithm in [hashes.SHA256(), hashes.SHA1()]:
            fingerprint = certificate.fingerprint(algorithm)
            print(f"  {algorithm.name}: {fingerprint.hex()}")

        # Additional Certificates
        if additional_certificates:
            print(f"\nNumber of Additional Certificates: {len(additional_certificates)}")
            for i, cert in enumerate(additional_certificates, 1):
                print(f"\nAdditional Certificate {i}:")
                print(f"  Subject: {cert.subject.rfc4514_string()}")
                print(f"  Issuer: {cert.issuer.rfc4514_string()}")
                print(f"  Serial Number: {cert.serial_number}")

    else:
        print("No certificate found in the PFX file.")


