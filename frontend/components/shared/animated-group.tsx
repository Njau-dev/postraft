"use client"

import type React from "react"

import { motion, type Variants } from "framer-motion"
import { cn } from "@/lib/utils"

interface AnimatedGroupProps {
    children: React.ReactNode
    className?: string
    variants?: {
        item: Variants,
        container?: Variants
    }
}

const defaultVariants = {
    container: {
        hidden: { opacity: 0 },
        visible: {
            opacity: 1,
            transition: {
                staggerChildren: 0.1,
                delayChildren: 0.3,
            },
        },
    },
    item: {
        hidden: { opacity: 0, y: 20 },
        visible: {
            opacity: 1,
            y: 0,
            transition: { duration: 0.5 },
        },
    },
}

export function AnimatedGroup({ children, className, variants }: AnimatedGroupProps) {
    const itemVariants = variants?.item || defaultVariants.item

    return (
        <motion.div className={cn(className)} initial="hidden" animate="visible" variants={defaultVariants.container}>
            <motion.div variants={itemVariants}>{children}</motion.div>
        </motion.div>
    )
}
