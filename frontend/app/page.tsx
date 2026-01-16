import HeroHeader from "@/components/marketing/header"
import FeaturesSection from "@/components/marketing/features"
import Pricing from "@/components/marketing/pricing"
import Testimonials from "@/components/marketing/testimonials"
import FAQ from "@/components/marketing/faq"
import CTA from "@/components/marketing/cta"
import Footer from "@/components/marketing/footer"
import HeroSection from "@/components/marketing/hero-section"

export default function HomePage() {
  return (
    <main className="min-h-screen">
      <HeroHeader />
      <HeroSection />
      <FeaturesSection />
      <Pricing />
      <Testimonials />
      <FAQ />
      <CTA />
      <Footer />
    </main>
  )
}
