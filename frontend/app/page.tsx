import HeroHeader from "@/components/marketing/header"
import FeaturesSection from "@/components/marketing/features"
import Pricing from "@/components/marketing/pricing"
import Testimonials from "@/components/marketing/testimonials"
import FAQ from "@/components/marketing/faq"
import CTA from "@/components/marketing/cta"
import Footer from "@/components/marketing/footer"
import HeroSection from "@/components/marketing/hero-section"
import IntegrationsSection from "@/components/marketing/integrations"

export default function LandingPage() {
  return (
    <main className="min-h-screen">
      <HeroHeader />
      <HeroSection />
      <FeaturesSection />
      <IntegrationsSection />
      <Pricing />
      <Testimonials />
      <FAQ />
      <CTA />
      <Footer />
    </main>
  )
}
