// 'use client';

// import { useAuth } from '@/hooks/useAuth';
// import DashboardHeader from '@/components/dashboard/dashboard-header';
// import StatsCard from '@/components/dashboard/stats-card';
// import RecentActivity from '@/components/dashboard/recent-activity';
// import { Button } from '@/components/ui/button';
// import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
// import { Package, Layout, ImageIcon, TrendingUp, Plus } from 'lucide-react';
// import Link from 'next/link';

// export default function DashboardPage() {
//   const { user, plan } = useAuth();

//   // Mock data - we'll replace with real data later
//   const stats = {
//     products: 0,
//     templates: 3, // System templates
//     posters: 0,
//     generations: user?.monthly_generations || 0,
//   };

//   return (
//     <div className="flex flex-col h-full">
//       <DashboardHeader
//         title="Dashboard"
//         description={`Welcome back, ${user?.email}`}
//       />

//       <main className="flex-1 overflow-y-auto p-6">
//           {/* Quick Actions */}
//           <Card>
//             <CardHeader>
//               <CardTitle>Quick Actions</CardTitle>
//             </CardHeader>
//             <CardContent>
//               <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
//                 <Link href="/products/add">
//                   <Button className="w-full bg-transparent" variant="outline">
//                     <Plus className="mr-2 h-4 w-4" />
//                     Add Product
//                   </Button>
//                 </Link>
//                 <Link href="/templates">
//                   <Button className="w-full bg-transparent" variant="outline">
//                     <Layout className="mr-2 h-4 w-4" />
//                     Browse Templates
//                   </Button>
//                 </Link>
//                 <Link href="/campaigns/create">
//                   <Button className="w-full bg-transparent" variant="outline">
//                     <Plus className="mr-2 h-4 w-4" />
//                     Create Campaign
//                   </Button>
//                 </Link>
//                 <Link href="/posters/generate">
//                   <Button className="w-full">
//                     <ImageIcon className="mr-2 h-4 w-4" />
//                     Generate Posters
//                   </Button>
//                 </Link>
//               </div>
//             </CardContent>
//           </Card>

//           {/* Two Column Layout */}
//           <div className="grid gap-6 md:grid-cols-2">
//             {/* Getting Started */}
//             <Card>
//               <CardHeader>
//                 <CardTitle>Getting Started</CardTitle>
//               </CardHeader>
//               <CardContent className="space-y-3">
//                 <div className="flex items-start gap-3">
//                   <div className="flex h-6 w-6 items-center justify-center rounded-full bg-primary text-xs text-primary-foreground">
//                     1
//                   </div>
//                   <div className="flex-1">
//                     <p className="text-sm font-medium">Add your first product</p>
//                     <p className="text-xs text-muted-foreground">
//                       Upload product images and details
//                     </p>
//                   </div>
//                   <Link href="/products/add">
//                     <Button size="sm" variant="ghost">
//                       Start
//                     </Button>
//                   </Link>
//                 </div>

//                 <div className="flex items-start gap-3">
//                   <div className="flex h-6 w-6 items-center justify-center rounded-full bg-muted text-xs">
//                     2
//                   </div>
//                   <div className="flex-1">
//                     <p className="text-sm font-medium">Choose a template</p>
//                     <p className="text-xs text-muted-foreground">
//                       Select from our professional designs
//                     </p>
//                   </div>
//                   <Link href="/templates">
//                     <Button size="sm" variant="ghost">
//                       Browse
//                     </Button>
//                   </Link>
//                 </div>

//                 <div className="flex items-start gap-3">
//                   <div className="flex h-6 w-6 items-center justify-center rounded-full bg-muted text-xs">
//                     3
//                   </div>
//                   <div className="flex-1">
//                     <p className="text-sm font-medium">Generate posters</p>
//                     <p className="text-xs text-muted-foreground">
//                       Create beautiful marketing materials
//                     </p>
//                   </div>
//                   <Link href="/posters/generate">
//                     <Button size="sm" variant="ghost">
//                       Generate
//                     </Button>
//                   </Link>
//                 </div>
//               </CardContent>
//             </Card>

//             {/* Recent Activity */}
//             <RecentActivity activities={[]} />
//           </div>

//           {/* Upgrade Prompt (if on Free plan) */}
//           {plan?.name === 'Free' && (
//             <Card className="border-primary/50 bg-primary/5">
//               <CardHeader>
//                 <CardTitle>Upgrade Your Plan</CardTitle>
//               </CardHeader>
//               <CardContent>
//                 <p className="text-sm text-muted-foreground mb-4">
//                   Unlock unlimited products, templates, and generations with our Pro plan.
//                 </p>
//                 <div className="flex gap-4">
//                   <Link href="/settings/billing">
//                     <Button>View Plans</Button>
//                   </Link>
//                   <Button variant="outline">Learn More</Button>
//                 </div>
//               </CardContent>
//             </Card>
//           )}
//         </div>
//       </main>
//     </div>
//   );
// }


import { SectionCards } from '@/components/dashboard/section-cards';

export default function DashboardPage() {
  return (
    <main className="@container/main flex flex-1 flex-col gap-2">
      <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">
        <SectionCards />
      </div>
    </main>
  );
}
