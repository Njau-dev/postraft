"use client"

import * as React from "react"

import { NavMain } from '@/components/dashboard/nav-main'
import { NavSecondary } from '@/components/dashboard/nav-secondary'
import { NavUser } from '@/components/dashboard/nav-user'
import {
    Sidebar,
    SidebarContent,
    SidebarFooter,
    SidebarHeader,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
} from '@/components/ui/side-bar'
import { Calendar, Image, Layout, LayoutDashboard, Megaphone, Package, Settings } from "lucide-react"
import { LogoIcon } from "../logo"
import { useAuth } from "@/contexts/AuthContext"

interface NavItem {
    title: string;
    url: string;
    icon: React.ComponentType<{ className?: string }>;
}

const navMain: NavItem[] = [
    {
        title: 'Dashboard',
        url: '/dashboard',
        icon: LayoutDashboard,
    },
    {
        title: 'Products',
        url: '/products',
        icon: Package,
    },
    {
        title: 'Templates',
        url: '/templates',
        icon: Layout,
    },
    {
        title: 'Campaigns',
        url: '/campaigns',
        icon: Megaphone,
    },
    {
        title: 'Posters',
        url: '/posters',
        icon: Image,
    },
    {
        title: 'Calendar',
        url: '/calendar',
        icon: Calendar,
    },
]
const navSecondary: NavItem[] = [
    {
        title: "Settings",
        url: "/settings",
        icon: Settings,
    },
]


export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
    const { user } = useAuth();
    return (
        <Sidebar collapsible="offcanvas" {...props}>
            <SidebarHeader>
                <SidebarMenu>
                    <SidebarMenuItem>
                        <SidebarMenuButton
                            asChild
                            className="data-[slot=sidebar-menu-button]:p-1.5!"
                        >
                            <a href="/dashboard">
                                <LogoIcon className="h-6 w-6" />
                                <span className="text-base font-semibold">Postraft</span>
                            </a>
                        </SidebarMenuButton>
                    </SidebarMenuItem>
                </SidebarMenu>
            </SidebarHeader>
            <SidebarContent>
                <NavMain items={navMain} />
                <NavSecondary items={navSecondary} className="mt-auto" />
            </SidebarContent>
            <SidebarFooter>
                {user && <NavUser user={user} />}
            </SidebarFooter>
        </Sidebar>
    )
}
