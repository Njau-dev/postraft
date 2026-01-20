'use client'

import { useState } from "react"
import Link from "next/link"

import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import {
    Field,
    FieldDescription,
    FieldGroup,
    FieldLabel,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { useAuth } from "@/hooks/useAuth"

export function ForgotPasswordForm({
    className,
    ...props
}: React.ComponentProps<"form">) {
    const { forgotPassword } = useAuth()

    const [email, setEmail] = useState("")
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState("")
    const [success, setSuccess] = useState("")

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError("")
        setSuccess("")

        setLoading(true)

        try {
            await forgotPassword(email)
            setSuccess("If an account exists for this email, a reset link has been sent.")
        } catch (err: any) {
            setError(
                err?.response?.data?.error ||
                "Failed to send password reset email"
            )
        } finally {
            setLoading(false)
        }
    }

    return (
        <form
            onSubmit={handleSubmit}
            className={cn("flex flex-col gap-6", className)}
            {...props}
        >
            <FieldGroup>
                <div className="flex flex-col items-center gap-1 text-center">
                    <h1 className="text-2xl font-bold">Forgot your password?</h1>
                    <p className="text-muted-foreground text-sm text-balance">
                        Enter your email and we&apos;ll send you a reset link.
                    </p>
                </div>

                {error && (
                    <Alert variant="destructive">
                        <AlertDescription>{error}</AlertDescription>
                    </Alert>
                )}

                {success && (
                    <Alert>
                        <AlertDescription>{success}</AlertDescription>
                    </Alert>
                )}

                <Field>
                    <FieldLabel htmlFor="email">Email address</FieldLabel>
                    <Input
                        id="email"
                        type="email"
                        placeholder="you@example.com"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        disabled={loading}
                        required
                    />
                    <FieldDescription>
                        We&apos;ll send a password reset link to this email.
                    </FieldDescription>
                </Field>

                <Field>
                    <Button type="submit" disabled={loading}>
                        {loading ? "Sending link..." : "Send reset link"}
                    </Button>
                </Field>

                <Field>
                    <FieldDescription className="px-6 text-center">
                        Remembered your password?{" "}
                        <Link href="/login" className="underline">
                            Back to login
                        </Link>
                    </FieldDescription>
                </Field>
            </FieldGroup>
        </form>
    )
}
