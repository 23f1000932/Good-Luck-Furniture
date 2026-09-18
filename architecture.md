# Good Luck Furniture — System Architecture

## 1. Project Overview

**Good Luck Furniture** is a premium furniture business website for showcasing the company's products, categories, brand story, showroom information, and contact details.

The website has two distinct experiences:

1. **Public storefront** — customers browse furniture, categories, product details, and contact the business.
2. **Admin dashboard** — authorized staff log in and manage products, categories, images, featured products, and basic website content.

The design goal is a **luxury, established furniture showroom aesthetic**, not a generic AI-generated SaaS/portfolio interface.

---

## 2. Core Design Direction

### Visual personality

The website should feel:

- Premium
- Warm
- Sophisticated
- Architectural
- Editorial
- Timeless
- Trustworthy
- Photography-led

Avoid:

- Generic AI landing-page layouts
- Excessive gradients
- Neon colors
- Glassmorphism everywhere
- Overuse of rounded cards
- Excessive shadows
- Huge meaningless headings
- Generic stock illustrations
- SaaS-style dashboards on the customer-facing website
- Random decorative animations
- "Made by AI" visual patterns

### Suggested visual system

Use a restrained palette such as:

- Warm ivory / off-white
- Deep charcoal
- Walnut / espresso brown
- Muted brass or champagne accent
- Natural neutral tones

Typography should combine:

- An elegant serif/display typeface for major editorial headings
- A clean sans-serif for navigation, descriptions, labels, and UI

Photography should dominate the visual language.

---

## 3. High-Level Architecture

```text
                         ┌─────────────────────────┐
                         │      Customer Browser   │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │     Vue 3 Frontend      │
                         │   Vite + Vue Router     │
                         └────────────┬────────────┘
                                      │ HTTPS / REST API
                                      ▼
                         ┌─────────────────────────┐
                         │      Flask Backend      │
                         │ REST API + Auth + CRUD  │
                         └───────┬─────────┬───────┘
                                 │         │
                    SQLAlchemy   │         │ Image upload
                                 │         ▼
                                 │  ┌──────────────────────┐
                                 │  │ Supabase Storage      │
                                 │  │ Product Images        │
                                 │  └──────────────────────┘
                                 │
                                 ▼
                       ┌─────────────────────────┐
                       │ PostgreSQL / Supabase   │
                       │ Product + Category DB   │
                       └─────────────────────────┘
```

### Development environment

```text
Vue 3
   │
   │ REST API
   ▼
Flask
   │
   ▼
SQLite
```

### Production environment

```text
Vue 3 frontend
      │
      ▼
Flask API
      │
      ├──────────────► Supabase PostgreSQL
      │
      └──────────────► Supabase Storage
                         │
                         ▼
                    Product Images
```

---

## 4. Technology Stack

### Frontend

- Vue 3
- Vite
- Vue Router
- Pinia where shared state is necessary
- Native `fetch` or Axios
- CSS architecture using scoped styles / CSS modules / well-structured global CSS
- Responsive design
- Lazy-loaded product images

### Backend

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate / Alembic
- Flask-JWT-Extended or secure session-based authentication
- Marshmallow or Pydantic-style validation
- Flask-CORS
- Werkzeug password hashing

### Database

Development:

- SQLite

Production:

- PostgreSQL through Supabase

### Image storage

Development:

- Local filesystem or configurable local upload directory

Production:

- Supabase Storage

**Important:** Do not store large image binaries directly inside PostgreSQL unless there is a strong reason to do so. Store images in object storage and keep their URLs/path metadata in PostgreSQL.

### Deployment

Recommended:

- Vue frontend → Vercel
- Flask backend → Render / Railway / similar Python hosting
- PostgreSQL → Supabase
- Images → Supabase Storage

---

## 5. Public Website Structure

### `/`

Homepage

Sections:

1. Premium hero
2. Brand introduction
3. Featured collections
4. Category showcase
5. Selected products
6. Why Good Luck Furniture
7. Showroom / business information
8. Contact CTA
9. Footer

The homepage should immediately communicate that Good Luck Furniture is a real, established furniture business.

---

### `/collections`

Collection/category landing page.

Possible categories:

- Bedroom Furniture
- Living Room Furniture
- Dining Room Furniture
- Office Furniture
- Home Decor
- Custom Furniture

The categories should be configurable rather than hard-coded where practical.

---

### `/products`

Product catalogue.

Features:

- Search
- Category filter
- Product-type filter
- Optional sort
- Responsive product grid
- Product image
- Product name
- Short description
- Optional price / "Contact for Price"
- Featured/new badges where appropriate

---

### `/products/:slug`

Product detail page.

Display:

- Large product gallery
- Product name
- Category
- Product type
- Description
- Dimensions
- Material
- Finish
- Color
- Availability
- Optional price
- Enquiry/contact CTA

Possible CTA:

> Enquire About This Product

This can open WhatsApp, phone, email, or a contact form depending on business requirements.

---

### `/about`

Business story.

Content can include:

- Company history
- Furniture philosophy
- Craftsmanship
- Quality
- Customer service
- Showroom information

Keep the copy human and business-specific. Avoid generic AI-generated marketing language.

---

### `/contact`

Include:

- Business address
- Phone number
- WhatsApp
- Email
- Opening hours
- Google Maps location
- Contact/enquiry form if required

---

## 6. Product Taxonomy

Use two levels:

### Room / Collection

Examples:

```text
Bedroom
Living Room
Dining Room
Office
Outdoor
Decor
```

### Product Type

Examples:

```text
Beds
Wardrobes
Dressing Tables
Sofas
Sofa Sets
Coffee Tables
TV Units
Dining Tables
Dining Chairs
Office Chairs
Study Tables
Side Tables
Cabinets
```

A product can belong to:

- One primary collection
- One product type

If future requirements need many-to-many relationships, introduce a join table rather than duplicating category data.

---

## 7. Database Model

### AdminUser

```text
id
email
password_hash
name
role
is_active
created_at
updated_at
last_login_at
```

Never store plain-text passwords.

---

### Category

```text
id
name
slug
description
image_url
display_order
is_active
created_at
updated_at
```

---

### Product

```text
id
name
slug
short_description
description
collection_id
product_type
material
finish
color
dimensions
price
price_visibility
is_featured
is_active
display_order
created_at
updated_at
```

`price_visibility` can support values such as:

```text
visible
contact_for_price
hidden
```

---

### ProductImage

```text
id
product_id
image_url
storage_path
alt_text
display_order
is_primary
created_at
```

This allows each product to have multiple images.

---

## 8. API Architecture

Base URL:

```text
/api
```

### Public endpoints

```text
GET    /api/products
GET    /api/products/:slug
GET    /api/categories
GET    /api/categories/:slug
GET    /api/featured-products
```

Optional:

```text
GET    /api/settings
POST   /api/contact
```

---

### Authentication

```text
POST   /api/auth/login
POST   /api/auth/logout
GET    /api/auth/me
```

Authentication should protect all admin mutation endpoints.

---

### Admin product endpoints

```text
GET    /api/admin/products
POST   /api/admin/products
GET    /api/admin/products/:id
PUT    /api/admin/products/:id
DELETE /api/admin/products/:id
```

### Admin image endpoints

```text
POST   /api/admin/products/:id/images
DELETE /api/admin/products/:id/images/:image_id
PUT    /api/admin/products/:id/images/reorder
```

### Admin category endpoints

```text
GET    /api/admin/categories
POST   /api/admin/categories
PUT    /api/admin/categories/:id
DELETE /api/admin/categories/:id
```

---

## 9. Image Upload Flow

### Development

```text
Admin Dashboard
      │
      ▼
Flask API
      │
      ▼
Validate image
      │
      ▼
Save to local uploads/
      │
      ▼
Save image metadata in SQLite
```

### Production

```text
Admin Dashboard
      │
      ▼
Flask API
      │
      ▼
Validate image
      │
      ▼
Upload to Supabase Storage
      │
      ▼
Receive storage URL/path
      │
      ▼
Save URL/path in PostgreSQL
```

Validation should include:

- Allowed MIME types
- Maximum file size
- Image dimensions where appropriate
- Safe filenames
- Server-side validation
- Optional image compression/resizing

Recommended formats:

```text
JPEG
PNG
WebP
```

For a furniture catalogue, WebP/AVIF delivery should be preferred where supported for performance.

---

## 10. Admin Dashboard

Admin routes should be separated from the public website.

Suggested routes:

```text
/admin/login
/admin
/admin/products
/admin/products/new
/admin/products/:id/edit
/admin/categories
/admin/settings
```

### Dashboard

Show:

- Total products
- Active products
- Featured products
- Categories
- Recent additions

Keep the admin UI functional and clean. It does not need to visually match the luxury storefront exactly.

---

## 11. Authentication & Security

Required:

- Password hashing using Werkzeug/PBKDF2 or Argon2/bcrypt
- HTTPS in production
- Secure authentication cookies or short-lived JWTs
- Authorization middleware
- CORS restricted to the frontend origin
- Input validation
- File upload validation
- Protection against SQL injection through SQLAlchemy
- CSRF protection if cookie-based authentication is used
- Rate limiting on login
- No secrets committed to Git
- Environment variables for credentials
- Secure error handling

Example environment variables:

```env
FLASK_ENV=development
DATABASE_URL=
SECRET_KEY=
JWT_SECRET_KEY=

SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
SUPABASE_STORAGE_BUCKET=
```

Never expose the Supabase service-role key in the Vue frontend.

---

## 12. Frontend Architecture

Suggested structure:

```text
frontend/
├── src/
│   ├── assets/
│   ├── components/
│   │   ├── layout/
│   │   ├── navigation/
│   │   ├── product/
│   │   ├── category/
│   │   └── common/
│   ├── views/
│   │   ├── HomeView.vue
│   │   ├── ProductsView.vue
│   │   ├── ProductDetailView.vue
│   │   ├── CategoriesView.vue
│   │   ├── AboutView.vue
│   │   ├── ContactView.vue
│   │   └── admin/
│   ├── router/
│   ├── stores/
│   ├── services/
│   │   ├── api.js
│   │   ├── products.js
│   │   ├── categories.js
│   │   └── auth.js
│   ├── composables/
│   ├── layouts/
│   ├── App.vue
│   └── main.js
```

---

## 13. Backend Architecture

Suggested structure:

```text
backend/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── models/
│   │   ├── admin_user.py
│   │   ├── category.py
│   │   ├── product.py
│   │   └── product_image.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── products.py
│   │   ├── categories.py
│   │   └── admin.py
│   ├── services/
│   │   ├── product_service.py
│   │   ├── image_service.py
│   │   └── auth_service.py
│   ├── schemas/
│   └── utils/
├── migrations/
├── tests/
├── run.py
├── requirements.txt
└── .env.example
```

Use application factory architecture so development, testing, and production configurations remain clean.

---

## 14. Environment Configuration

### Development

```text
Vue 3 + Vite
localhost:5173

Flask
localhost:5000

SQLite
local database file

Local image storage
```

### Production

```text
Vercel
    │
    ▼
Vue application

Render
    │
    ▼
Flask API
    │
    ├──► Supabase PostgreSQL
    │
    └──► Supabase Storage
```

Use environment-specific configuration rather than hard-coded URLs.

---

## 15. Responsive Design

The website must work well on:

- Desktop
- Laptop
- Tablet
- Mobile

Important mobile requirements:

- Mobile navigation
- Touch-friendly controls
- Responsive image galleries
- Product grid adapting to viewport
- No horizontal overflow
- Readable typography
- Sticky or easily accessible contact CTA
- Fast image loading

---

## 16. Performance

Because this is a photography-heavy furniture website:

- Use responsive image sizes
- Lazy-load below-the-fold images
- Use WebP/AVIF when possible
- Provide explicit image dimensions to reduce layout shift
- Avoid loading unnecessary JavaScript
- Lazy-load non-critical components
- Use route-level code splitting
- Cache public API responses where appropriate
- Paginate large product lists

Do not sacrifice image quality excessively. Furniture photography is a core part of the brand experience.

---

## 17. SEO

Each product should have:

- Unique title
- Meta description
- Clean slug
- Canonical URL
- Image alt text

Example:

```text
/products/solid-walnut-king-bed
```

Use semantic HTML.

The site should include:

- `robots.txt`
- XML sitemap
- Open Graph metadata
- Local business structured data where appropriate
- Product structured data where applicable

---

## 18. UX Principles

The public website should feel like browsing a premium furniture showroom.

Prioritize:

1. Photography
2. Product discovery
3. Clear categories
4. Product information
5. Trust
6. Easy contact

Avoid turning every section into a card grid.

Use:

- Large editorial photography
- Asymmetric layouts
- Generous whitespace
- Strong typography
- Subtle transitions
- Horizontal collection sections
- Full-width visual sections
- Carefully designed product grids

Animations should be subtle and purposeful.

---

## 19. Product Management UX

Admin should be able to:

- Create product
- Edit product
- Delete/deactivate product
- Upload multiple images
- Set primary image
- Reorder images
- Assign collection
- Set product type
- Add material
- Add finish
- Add dimensions
- Add optional price
- Mark product as featured
- Publish/unpublish product

Product form should provide clear validation and image previews.

---

## 20. API Response Convention

Use consistent JSON responses.

Success example:

```json
{
  "success": true,
  "data": {}
}
```

Error example:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Product name is required"
  }
}
```

Use appropriate HTTP status codes.

---

## 21. Error Handling

Frontend should gracefully handle:

- API unavailable
- Product not found
- Image loading failure
- Authentication failure
- Validation errors
- Upload failure
- Empty product catalogue

Do not expose stack traces or internal database errors to customers.

---

## 22. Testing

Backend:

- Authentication tests
- Product CRUD tests
- Category CRUD tests
- Image upload validation
- API response tests
- Authorization tests

Frontend:

- Router tests
- Product rendering tests
- Filter/search tests
- Admin authentication flow
- Form validation tests

End-to-end testing can be added after the core application is stable.

---

## 23. Deployment Checklist

### Frontend

- Production API URL configured
- Build succeeds
- SPA routing configured on hosting provider
- Images load correctly
- Mobile tested

### Backend

- Production WSGI server
- Environment variables configured
- Database migration applied
- CORS configured
- Authentication secrets configured
- Upload limits configured
- Logs enabled

### Supabase

- PostgreSQL configured
- Storage bucket created
- Storage policies reviewed
- Production credentials stored securely
- Database backups/settings reviewed

---

## 24. Important Architectural Decision

The phrase "database stores the image" should be implemented as:

> **PostgreSQL stores product/image metadata and the reference to the image; Supabase Storage stores the actual image files in production.**

This is more scalable and appropriate for a product catalogue than putting large binary image data directly into PostgreSQL.

For development, local files can be used so the project remains simple and inexpensive.

---

## 25. Implementation Priority

Build in this order:

### Phase 1 — Foundation

- Repository structure
- Vue + Vite
- Flask application factory
- SQLAlchemy
- SQLite configuration
- PostgreSQL/Supabase configuration
- Environment configuration

### Phase 2 — Public Website

- Navigation
- Homepage
- Categories
- Product listing
- Product detail
- About
- Contact
- Responsive design

### Phase 3 — Admin

- Admin login
- Authentication
- Dashboard
- Product CRUD
- Category management
- Image management

### Phase 4 — Production Storage

- Supabase Storage
- Image upload service
- PostgreSQL migration
- Production environment variables

### Phase 5 — Polish

- SEO
- Performance
- Accessibility
- Error states
- Loading states
- Animations
- Mobile refinement
- Security hardening

---

## 26. Definition of Done

The project is complete when:

- Customers can browse the business website without logging in.
- Customers can browse products by category.
- Customers can open detailed product pages.
- Product images are displayed in a premium gallery.
- Contact information is always easy to find.
- Admin can securely log in.
- Admin can create, update, publish/unpublish, and delete products.
- Admin can upload and manage multiple product images.
- Admin can manage categories.
- Development works with SQLite.
- Production works with Supabase PostgreSQL.
- Production images use Supabase Storage.
- No production secrets are exposed to the frontend.
- The website is responsive.
- The visual design feels like a real premium furniture showroom rather than an AI-generated template.
