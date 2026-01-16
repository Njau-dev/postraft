"use client"

import { motion, type Variants } from "framer-motion"
import { cn } from "@/lib/utils"

type PresetType = "fade-in-blur" | "fade" | "slide-up"

const presets: Record<PresetType, Variants> = {
    "fade-in-blur": {
        hidden: { opacity: 0, filter: "blur(12px)", y: 12 },
        visible: (i: number) => ({
            opacity: 1,
            filter: "blur(0px)",
            y: 0,
            transition: { delay: i * 0.05, duration: 0.4 },
        }),
    },
    fade: {
        hidden: { opacity: 0 },
        visible: (i: number) => ({
            opacity: 1,
            transition: { delay: i * 0.05, duration: 0.4 },
        }),
    },
    "slide-up": {
        hidden: { opacity: 0, y: 20 },
        visible: (i: number) => ({
            opacity: 1,
            y: 0,
            transition: { delay: i * 0.05, duration: 0.4 },
        }),
    },
}

interface TextEffectProps {
    children: string
    className?: string
    preset?: PresetType
    speedReveal?: number
    speedSegment?: number
}

export function TextEffect({
    children,
    className,
    preset = "fade-in-blur",
    speedReveal = 1,
    speedSegment = 0.3,
}: TextEffectProps) {
    const words = children.split(" ")
    const variants = presets[preset]

    return (
        <motion.h1 className={cn("flex flex-wrap justify-center gap-x-2", className)} initial="hidden" animate="visible">
            {words.map((word, i) => (
                <motion.span
                    key={i}
                    custom={i * speedSegment}
                    variants={variants}
                    style={{ transitionDuration: `${speedReveal}s` }}
                >
                    {word}
                </motion.span>
            ))}
        </motion.h1>
    )
}
