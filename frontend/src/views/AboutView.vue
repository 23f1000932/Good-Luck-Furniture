<template>
  <div class="about-view">
    <!-- Hero -->
    <section class="about-hero" aria-label="About Good Luck Furniture">
      <div class="about-hero__image-wrap">
        <img
          src="https://images.unsplash.com/photo-1524758631624-e2822e304c36?w=1600&q=80"
          alt="Good Luck Furniture showroom"
          class="about-hero__image img-cover"
          loading="eager"
          width="1600"
          height="900"
        />
        <div class="about-hero__tint" aria-hidden="true"></div>
      </div>
      <div class="about-hero__content container">
        <p class="section-label" style="color: rgba(240,235,227,0.7);">About Us</p>
        <h1 class="heading-lg about-hero__title">Good Luck Furniture</h1>
        <p class="about-hero__sub">Rajrooppur, Prayagraj</p>
      </div>
    </section>

    <!-- Story -->
    <section class="section about-story" aria-labelledby="story-heading">
      <div class="container container--narrow">
        <p class="section-label">Our Approach</p>
        <hr class="divider--brass" style="margin-block: 1.25rem;" />
        <h2 id="story-heading" class="heading-sm" style="margin-bottom: var(--space-8);">
          Furniture that earns its place
        </h2>
        <div class="about-body">
          <p>
            Good Luck Furniture is a furniture showroom in Rajrooppur, Prayagraj.
            We carry furniture for every room — beds and wardrobes for the bedroom,
            sofas and coffee tables for the living room, dining sets, office furniture,
            and decorative pieces for the rest of the home.
          </p>
          <p>
            Our showroom is open every day. Walk in, spend as long as you need,
            ask us anything. We'll tell you honestly what's worth the investment and
            what might suit your space better.
          </p>
          <p>
            We believe a furniture purchase shouldn't be rushed. The right piece,
            in the right material, at the right scale — that's what we help you find.
          </p>
        </div>
      </div>
    </section>

    <!-- Values -->
    <section class="section--sm values-section" style="background: var(--color-ivory-mid);" aria-labelledby="values-heading">
      <div class="container">
        <p class="section-label">What We Stand For</p>
        <hr class="divider--brass" style="margin-block: 1.25rem;" />
        <h2 id="values-heading" class="heading-sm" style="margin-bottom: var(--space-12);">Our principles</h2>
        <div class="values-grid">
          <div class="value-item">
            <div class="value-item__number">01</div>
            <h3 class="value-item__title">Honest materials</h3>
            <p class="value-item__desc">
              We tell you what each piece is made of — solid wood, engineered wood, MDF, fabric grade.
              No surprises after purchase.
            </p>
          </div>
          <div class="value-item">
            <div class="value-item__number">02</div>
            <h3 class="value-item__title">Right scale for your room</h3>
            <p class="value-item__desc">
              Furniture that's too large overwhelms a room. Too small and it disappears.
              We help you choose proportions that work.
            </p>
          </div>
          <div class="value-item">
            <div class="value-item__number">03</div>
            <h3 class="value-item__title">Long-term value</h3>
            <p class="value-item__desc">
              A well-chosen piece should last years, not seasons.
              We stock furniture that holds up under daily family life.
            </p>
          </div>
          <div class="value-item">
            <div class="value-item__number">04</div>
            <h3 class="value-item__title">Straightforward service</h3>
            <p class="value-item__desc">
              Visit the showroom, browse at your own pace, ask us questions.
              No pressure. No sales tactics. Just honest guidance.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Showroom -->
    <section class="section showroom-info" aria-labelledby="showroom-heading">
      <div class="container">
        <div class="showroom-split">
          <div class="showroom-split__text">
            <p class="section-label">Find Us</p>
            <hr class="divider--brass" style="margin-block: 1.25rem;" />
            <h2 id="showroom-heading" class="heading-sm">Visit our showroom</h2>
            <address class="showroom-details">
              <p><strong>Good Luck Furniture</strong></p>
              <p>Opposite Sai Dham Apartments,</p>
              <p>Rehmat Complex, Rajrooppur,</p>
              <p>Prayagraj, Uttar Pradesh 211015</p>
            </address>
            <div class="showroom-hours">
              <p><strong>Opening Hours</strong></p>
              <p>Monday to Sunday: 11 AM – 9 PM</p>
            </div>
            <div class="showroom-contact-links">
              <a href="tel:+919415612726" class="btn btn-primary">Call 9415612726</a>
              <a href="https://wa.me/919415612726" target="_blank" rel="noopener" class="btn btn-outline">WhatsApp</a>
            </div>
          </div>
          <div class="showroom-split__image">
            <div class="aspect-landscape overflow-hidden">
              <img
                src="https://images.unsplash.com/photo-1560185007-cde436f6a4d0?w=800&q=80"
                alt="Furniture showroom interior"
                class="img-cover"
                loading="lazy"
                width="800"
                height="600"
              />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="section--sm" style="background: var(--color-charcoal);" aria-labelledby="cta-heading">
      <div class="container text-center">
        <h2 id="cta-heading" class="heading-sm" style="color: var(--color-ivory); margin-bottom: var(--space-5);">
          Ready to furnish your home?
        </h2>
        <p style="color: var(--color-stone-light); margin-bottom: var(--space-8); max-width: 40ch; margin-inline: auto;">
          Browse our catalogue or visit us in person.
        </p>
        <div style="display: flex; gap: var(--space-4); justify-content: center; flex-wrap: wrap;">
          <RouterLink to="/products" class="btn btn-brass btn-lg">Browse Products</RouterLink>
          <RouterLink to="/contact" class="btn btn-outline" style="border-color: rgba(255,255,255,0.3); color: var(--color-ivory);">Get Directions</RouterLink>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
// About page — static content
</script>

<style scoped>
/* Hero */
.about-hero {
  position: relative;
  height: 60vh;
  min-height: 400px;
  display: flex;
  align-items: flex-end;
  padding-bottom: var(--space-16);
}

.about-hero__image-wrap {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.about-hero__image {
  width: 100%;
  height: 100%;
}

.about-hero__tint {
  position: absolute;
  inset: 0;
  background: rgba(26,26,26,0.55);
}

.about-hero__content {
  position: relative;
  z-index: 1;
}

.about-hero__title {
  color: var(--color-ivory);
  margin-top: var(--space-4);
  margin-bottom: var(--space-2);
}

.about-hero__sub {
  color: rgba(240,235,227,0.65);
  font-size: var(--text-sm);
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
}

/* Story */
.about-body {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.about-body p {
  color: var(--text-secondary);
  line-height: var(--leading-relaxed);
  font-size: var(--text-md);
}

/* Values */
.values-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-10);
}

.value-item__number {
  font-family: var(--font-display);
  font-size: var(--text-3xl);
  color: var(--color-brass-pale);
  line-height: 1;
  margin-bottom: var(--space-4);
}

.value-item__title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 400;
  margin-bottom: var(--space-3);
}

.value-item__desc {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  line-height: var(--leading-relaxed);
}

/* Showroom */
.showroom-split {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-20);
  align-items: center;
}

.showroom-details {
  font-style: normal;
  color: var(--text-secondary);
  line-height: var(--leading-relaxed);
  margin-top: var(--space-8);
  margin-bottom: var(--space-5);
}

.showroom-hours {
  color: var(--text-secondary);
  margin-bottom: var(--space-8);
  font-size: var(--text-sm);
  line-height: var(--leading-relaxed);
}

.showroom-contact-links {
  display: flex;
  gap: var(--space-3);
  flex-wrap: wrap;
}

@media (max-width: 900px) {
  .values-grid { grid-template-columns: 1fr 1fr; }
  .showroom-split { grid-template-columns: 1fr; gap: var(--space-10); }
}

@media (max-width: 600px) {
  .values-grid { grid-template-columns: 1fr; }
}
</style>
