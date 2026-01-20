'use client'

import { useState } from "react"
import Link from "next/link"

import { cn } from "@/lib/utils"
import { useAuth } from "@/hooks/useAuth"
import { Button } from "@/components/ui/button"
import {
    Field,
    FieldDescription,
    FieldGroup,
    FieldLabel,
    FieldSeparator,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { Alert, AlertDescription } from "@/components/ui/alert"

export function RegisterForm({
    className,
    ...props
}: React.ComponentProps<"form">) {
    const { register } = useAuth()

    const [email, setEmail] = useState("")
    const [userName, setUserName] = useState("")
    const [password, setPassword] = useState("")
    const [confirmPassword, setConfirmPassword] = useState("")
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState("")

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError("")

        if (!userName.trim()) {
            setError("Name is required")
            return
        }

        if (userName.length < 2) {
            setError("Name must be at least 2 characters")
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
            await register(email, password, userName)
        } catch (err: any) {
            setError(err?.response?.data?.error || "Registration failed")
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
                    <h1 className="text-2xl font-bold">Create your account</h1>
                    <p className="text-muted-foreground text-sm text-balance">
                        Start generating professional posters today
                    </p>
                </div>

                {error && (
                    <Alert variant="destructive">
                        <AlertDescription>{error}</AlertDescription>
                    </Alert>
                )}

                <Field>
                    <FieldLabel htmlFor="email">Email</FieldLabel>
                    <Input
                        id="email"
                        type="email"
                        placeholder="mail@example.com"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        disabled={loading}
                        required
                    />
                </Field>

                <Field>
                    <FieldLabel htmlFor="userName">Full Name</FieldLabel>
                    <Input
                        id="userName"
                        type="text"
                        placeholder="John Doe"
                        value={userName}
                        onChange={(e) => setUserName(e.target.value)}
                        disabled={loading}
                        required
                    />
                </Field>

                <Field>
                    <FieldLabel htmlFor="password">Password</FieldLabel>
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
                    <FieldLabel htmlFor="confirmPassword">Confirm Password</FieldLabel>
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
                        {loading ? "Creating account..." : "Create account"}
                    </Button>
                </Field>

                <FieldSeparator>Or continue with</FieldSeparator>

                <Field>
                    <Button variant="outline" type="button" disabled={loading}>
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 48 48"
                            className="size-5"
                        >
                            <path
                                fill="#EA4335"
                                d="M24 9.5c3.54 0 6.7 1.22 9.18 3.22l6.82-6.82C35.82 2.36 30.24 0 24 0 14.64 0 6.44 5.38 2.52 13.22l7.98 6.2C12.28 13.02 17.7 9.5 24 9.5z"
                            />
                            <path
                                fill="#34A853"
                                d="M46.5 24c0-1.64-.14-3.22-.4-4.76H24v9.02h12.7c-.56 3-2.26 5.54-4.82 7.24l7.38 5.72C43.92 36.9 46.5 30.9 46.5 24z"
                            />
                            <path
                                fill="#FBBC05"
                                d="M10.5 28.98c-.5-1.5-.78-3.1-.78-4.98s.28-3.48.78-4.98l-7.98-6.2C.92 16.14 0 19.98 0 24s.92 7.86 2.52 11.18l7.98-6.2z"
                            />
                            <path
                                fill="#4285F4"
                                d="M24 48c6.24 0 11.82-2.06 15.76-5.6l-7.38-5.72c-2.06 1.38-4.7 2.2-8.38 2.2-6.3 0-11.72-3.52-13.5-8.42l-7.98 6.2C6.44 42.62 14.64 48 24 48z"
                            />
                        </svg>
                        Sign up with Google
                    </Button>

                    <FieldDescription className="px-6 text-center">
                        Already have an account?{" "}
                        <Link href="/login" className="underline">
                            Sign in
                        </Link>
                    </FieldDescription>
                </Field>
            </FieldGroup>
        </form>
    )
}
