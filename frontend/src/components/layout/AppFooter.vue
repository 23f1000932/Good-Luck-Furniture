<template>
  <footer class="footer">
    <div class="container">
      <div class="footer__grid">
        <!-- Brand -->
        <div class="footer__brand">
          <RouterLink to="/" class="footer__logo">Good Luck Furniture</RouterLink>
          <p class="footer__tagline">Quality furniture for every room.<br>Visit our showroom in Prayagraj.</p>
          <div class="footer__social">
            <a href="https://wa.me/919415612726" target="_blank" rel="noopener" class="footer__social-link" aria-label="WhatsApp">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
              </svg>
            </a>
            <a href="tel:+919415612726" class="footer__social-link" aria-label="Call us">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
                <path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 013.07 9.81a19.79 19.79 0 01-3.07-8.66A2 2 0 012 .18h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L6.09 7.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7a2 2 0 011.72 2.03z"/>
              </svg>
            </a>
          </div>
        </div>

        <!-- Collections -->
        <div class="footer__col">
          <h4 class="footer__heading">Collections</h4>
          <ul class="footer__links">
            <li><RouterLink to="/collections" class="footer__link">All Collections</RouterLink></li>
            <li><RouterLink to="/products?collection=bedroom" class="footer__link">Bedroom</RouterLink></li>
            <li><RouterLink to="/products?collection=living-room" class="footer__link">Living Room</RouterLink></li>
            <li><RouterLink to="/products?collection=dining-room" class="footer__link">Dining Room</RouterLink></li>
            <li><RouterLink to="/products?collection=office" class="footer__link">Office</RouterLink></li>
          </ul>
        </div>

        <!-- Navigation -->
        <div class="footer__col">
          <h4 class="footer__heading">Navigation</h4>
          <ul class="footer__links">
            <li><RouterLink to="/" class="footer__link">Home</RouterLink></li>
            <li><RouterLink to="/products" class="footer__link">Products</RouterLink></li>
            <li><RouterLink to="/about" class="footer__link">About</RouterLink></li>
            <li><RouterLink to="/contact" class="footer__link">Contact</RouterLink></li>
          </ul>
        </div>

        <!-- Contact -->
        <div class="footer__col">
          <h4 class="footer__heading">Visit Us</h4>
          <address class="footer__address">
            <p>Opposite Sai Dham Apartments,</p>
            <p>Rehmat Complex, Rajrooppur,</p>
            <p>Prayagraj, UP 211015</p>
          </address>
          <div class="footer__contact-links">
            <a href="tel:+919415612726" class="footer__contact-item">
              <span>9415612726</span>
            </a>
            <a href="mailto:abadhussain4212@gmail.com" class="footer__contact-item">
              <span>abadhussain4212@gmail.com</span>
            </a>
            <p class="footer__hours">Mon – Sun &nbsp;|&nbsp; 11 AM – 9 PM</p>
          </div>
        </div>
      </div>

      <hr class="divider footer__divider" />

      <div class="footer__bottom">
        <p class="footer__copy">
          © {{ currentYear }} Good Luck Furniture. All rights reserved.
        </p>
        <p class="footer__credits">
          Prayagraj, Uttar Pradesh
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup>
const currentYear = new Date().getFullYear()
</script>

<style scoped>
.footer {
  background: var(--color-charcoal);
  color: var(--color-ivory-mid);
  padding-top: var(--space-20);
  padding-bottom: var(--space-10);
}

.footer__grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1.5fr;
  gap: var(--space-12);
  margin-bottom: var(--space-16);
}

.footer__logo {
  display: block;
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 500;
  color: var(--color-ivory);
  margin-bottom: var(--space-4);
  letter-spacing: var(--tracking-tight);
  transition: color var(--transition-fast);
}

.footer__logo:hover {
  color: var(--color-brass-light);
}

.footer__tagline {
  font-size: var(--text-sm);
  color: var(--color-stone-light);
  line-height: var(--leading-relaxed);
  margin-bottom: var(--space-6);
}

.footer__social {
  display: flex;
  gap: var(--space-3);
}

.footer__social-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: var(--radius-sm);
  color: var(--color-stone-light);
  transition: all var(--transition-base);
}

.footer__social-link:hover {
  background: var(--color-brass);
  border-color: var(--color-brass);
  color: var(--color-white);
}

.footer__heading {
  font-family: var(--font-sans);
  font-size: var(--text-xs);
  font-weight: 500;
  letter-spacing: var(--tracking-widest);
  text-transform: uppercase;
  color: var(--color-stone-light);
  margin-bottom: var(--space-5);
}

.footer__links {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.footer__link {
  font-size: var(--text-sm);
  color: var(--color-mist);
  transition: color var(--transition-fast);
}

.footer__link:hover {
  color: var(--color-ivory);
}

.footer__address {
  font-style: normal;
  font-size: var(--text-sm);
  color: var(--color-mist);
  line-height: var(--leading-relaxed);
  margin-bottom: var(--space-5);
}

.footer__contact-links {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.footer__contact-item {
  font-size: var(--text-sm);
  color: var(--color-mist);
  transition: color var(--transition-fast);
}

.footer__contact-item:hover {
  color: var(--color-ivory);
}

.footer__hours {
  font-size: var(--text-xs);
  color: var(--color-stone);
  margin-top: var(--space-2);
}

.footer__divider {
  background: rgba(255,255,255,0.08);
  margin-bottom: var(--space-8);
}

.footer__bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.footer__copy,
.footer__credits {
  font-size: var(--text-xs);
  color: var(--color-stone);
}

/* ─── Responsive ──────────────────── */
@media (max-width: 900px) {
  .footer__grid {
    grid-template-columns: 1fr 1fr;
    gap: var(--space-10);
  }
  .footer__brand {
    grid-column: 1 / -1;
  }
}

@media (max-width: 540px) {
  .footer__grid {
    grid-template-columns: 1fr;
    gap: var(--space-8);
  }
  .footer__bottom {
    flex-direction: column;
    gap: var(--space-2);
    text-align: center;
  }
}
</style>
