import random
class DiffieHellman:
    def _is_prime(self, n):
        if n < 2:
            return False
        if n < 4:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    def generate(self, max_mod=None):
        """Generate DH parameters (mod, gen). Returns (p, g)."""
        if max_mod is None:
            max_mod = 1000
        primes = [p for p in range(3, max_mod) if self._is_prime(p)]
        modularWord = random.choice(primes)
        generator = random.randint(2, modularWord - 1)
        return modularWord, generator

    def halfkey(self, mod, gen, privateNumber=None):
        """Compute DH half key: A = g^a mod p. Returns (A, a)."""
        if privateNumber is None:
            privateNumber = random.randint(2, mod - 2)
        half_key = pow(gen, privateNumber, mod)
        return half_key, privateNumber

    def secret(self, modularWord, generator, privateNumber, ServerHalfKey):
        """Compute DH shared secret: s = gB^a mod p."""
        return pow(ServerHalfKey, privateNumber,modularWord)
