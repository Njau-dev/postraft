import ProtectedRoute from '@/components/shared/protected-route';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-slate-50">
        {/* We'll add sidebar and header in Day 5 */}

        {children}
      </div>
    </ProtectedRoute>
  );
}
