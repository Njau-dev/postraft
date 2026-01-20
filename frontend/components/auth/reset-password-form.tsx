'use client'

import { useState } from "react"
import { useSearchParams, useRouter } from "next/navigation"
import Link from "next/link"

import { cn } from "@/lib/utils"
import { useAuth } from "@/hooks/useAuth"
import { Button } from "@/components/ui/button"
import {
    Field,
    FieldDescription,
    FieldGroup,
    FieldLabel,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { Alert, AlertDescription } from "@/components/ui/alert"

export function ResetPasswordForm({
    className,
    ...props
}: React.ComponentProps<"form">) {
    const { resetPassword } = useAuth()
    const searchParams = useSearchParams()
    const router = useRouter()

    const token = searchParams.get("token")

    const [password, setPassword] = useState("")
    const [confirmPassword, setConfirmPassword] = useState("")
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState("")
    const [success, setSuccess] = useState("")

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError("")
        setSuccess("")

        if (!token) {
            setError("Invalid or missing reset token")
            return
        }

        if (password !== confirmPassword) {
            setError("Passwords do not match")
            return
        }

        if (password.length < 8) {
            setError("Password must be at least 8 characters")
            return
        }

        setLoading(true)

        try {
            await resetPassword(token, password)
            setSuccess("Password reset successful. Redirecting to login...")

            setTimeout(() => {
                router.push("/login")
            }, 1500)
        } catch (err: any) {
            setError(
                err?.response?.data?.error ||
                "Failed to reset password"
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
                    <h1 className="text-2xl font-bold">Reset your password</h1>
                    <p className="text-muted-foreground text-sm">
                        Enter a new password for your account
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
                    <FieldLabel htmlFor="password">New Password</FieldLabel>
                    <Input
                        id="password"
                        type="password"
                        placeholder="••••••••"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        disabled={loading}
                        required
                    />
                    <FieldDescription>
                        Must be at least 8 characters long.
                    </FieldDescription>
                </Field>

                <Field>
                    <FieldLabel htmlFor="confirmPassword">
                        Confirm New Password
                    </FieldLabel>
                    <Input
                        id="confirmPassword"
                        type="password"
                        placeholder="••••••••"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        disabled={loading}
                        required
                    />
                </Field>

                <Field>
                    <Button type="submit" disabled={loading}>
                        {loading ? "Resetting..." : "Reset password"}
                    </Button>
                </Field>

                <Field>
                    <FieldDescription className="px-6 text-center">
                        <Link href="/login" className="underline">
                            Back to login
                        </Link>
                    </FieldDescription>
                </Field>
            </FieldGroup>
        </form>
    )
}
