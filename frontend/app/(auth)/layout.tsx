import { GalleryVerticalEnd } from "lucide-react"
import Image from "next/image"

import { ThemeToggle } from "@/components/shared/theme-toggle"

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="grid min-h-svh lg:grid-cols-2">
      {/* Left side (content) */}
      <div className="flex flex-col gap-4 p-6 md:p-10">
        <div className="flex justify-between gap-2">
          <a href="/" className="flex items-center gap-2 font-medium">
            <div className="bg-primary text-primary-foreground flex size-6 items-center justify-center rounded-md">
              <GalleryVerticalEnd className="size-4" />
            </div>
            Post Raft.
          </a>
          <ThemeToggle />
        </div>

        <div className="flex flex-1 items-center justify-center">
          <div className="w-full max-w-xs">
            {children}
          </div>
        </div>
      </div>

      {/* Right side (background images) */}
      <div className="relative hidden lg:block overflow-hidden">
        <Image
          src="/images/night-background.webp"
          alt="night background"
          className="absolute inset-0 h-full w-full object-cover object-center hidden dark:block"
          width={3276}
          height={4095}
          priority
        />
        <Image
          src="/images/light-background.webp"
          alt="light background"
          className="absolute inset-0 h-full w-full object-cover object-top dark:hidden"
          width={3276}
          height={4095}
          priority
        />
      </div>
    </div>
  )
}
