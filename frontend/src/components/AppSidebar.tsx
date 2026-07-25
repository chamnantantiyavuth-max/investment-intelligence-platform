import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
} from "@/components/ui/sidebar"
import { LayoutDashboard, TrendingUp, Shield, Radio, DollarSign, Building2 } from "lucide-react"
import { Link, useLocation } from "react-router-dom"

const navItems = [
  { title: "Strategy Control Center", url: "/", icon: LayoutDashboard },
  { title: "Alpha Momentum Queue", url: "/am-queue", icon: TrendingUp },
  { title: "Close System Radar", url: "/cs-radar", icon: Shield },
  { title: "Fundamental Queue", url: "/fundamental", icon: Building2 },
  { title: "Cheap & Quality", url: "/cheap-quality", icon: DollarSign },
  { title: "Weak Signal Inbox", url: "/weak-signals", icon: Radio },
]

export function AppSidebar() {
  const location = useLocation()

  return (
    <Sidebar collapsible="icon" variant="sidebar">
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              size="lg"
              render={<Link to="/" />}
            >
              <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
                <TrendingUp className="size-4" />
              </div>
              <div className="flex flex-col gap-0.5 leading-none">
                <span className="font-semibold">IIP</span>
                <span className="text-xs text-sidebar-foreground/60">
                  Investment Intelligence
                </span>
              </div>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Navigation</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {navItems.map((item) => (
                <SidebarMenuItem key={item.url}>
                  <SidebarMenuButton
                    isActive={location.pathname === item.url}
                    tooltip={item.title}
                    render={<Link to={item.url} />}
                  >
                    <item.icon />
                    <span>{item.title}</span>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarRail />
    </Sidebar>
  )
}
