'use client';

import { useState } from 'react';
import { useTemplates, useDeleteTemplate, useDuplicateTemplate } from '@/hooks/useTemplates';
import EmptyState from '@/components/shared/empty-state';
import TemplateCard from '@/components/templates/TemplateCard';
import TemplatePreviewDialog from '@/components/templates/TemplatePreviewDialog';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Skeleton } from '@/components/ui/skeleton';
import {
  Layout,
  Plus,
  Loader2,
  Search,
  Filter,
  Grid3x3,
  List,
  Sparkles,
  Zap,
  Copy,
  Eye,
  Trash2,
  MoreHorizontal,
  Layers,
  Image as ImageIcon,
  TrendingUp,
  BookOpen,
  Users
} from 'lucide-react';
import { Template } from '@/types';
import { useAuth } from '@/hooks/useAuth';

export default function TemplatesPage() {
  const [selectedFormat, setSelectedFormat] = useState<string>('all');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [searchQuery, setSearchQuery] = useState('');
  const [previewTemplate, setPreviewTemplate] = useState<Template | null>(null);
  const [previewOpen, setPreviewOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [templateToDelete, setTemplateToDelete] = useState<Template | null>(null);

  const { user, plan } = useAuth();
  const { data: templates, isLoading, isError } = useTemplates(
    selectedFormat !== 'all' ? selectedFormat : undefined
  );
  const deleteTemplate = useDeleteTemplate();
  const duplicateTemplate = useDuplicateTemplate();

  // Filter templates based on search
  const filteredTemplates = templates?.filter(template =>
    template.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    template.description?.toLowerCase().includes(searchQuery.toLowerCase())
  ) || [];

  // Separate system and custom templates
  const systemTemplates = filteredTemplates.filter((t) => t.is_system);
  const customTemplates = filteredTemplates.filter((t) => !t.is_system);

  const handlePreview = (template: Template) => {
    setPreviewTemplate(template);
    setPreviewOpen(true);
  };

  const handleDuplicate = async (template: Template) => {
    await duplicateTemplate.mutateAsync(template.id);
  };

  const handleDelete = (template: Template) => {
    setTemplateToDelete(template);
    setDeleteDialogOpen(true);
  };

  const confirmDelete = async () => {
    if (templateToDelete) {
      await deleteTemplate.mutateAsync(templateToDelete.id);
      setDeleteDialogOpen(false);
      setTemplateToDelete(null);
    }
  };

  const handleViewModeChange = (mode: 'grid' | 'list') => {
    setViewMode(mode);
  };

  const formatStats = [
    { format: 'square', count: templates?.filter(t => t.format === 'square').length || 0, icon: Grid3x3 },
    { format: 'story', count: templates?.filter(t => t.format === 'story').length || 0, icon: TrendingUp },
    { format: 'a4', count: templates?.filter(t => t.format === 'a4').length || 0, icon: BookOpen },
    { format: 'custom', count: customTemplates.length, icon: Users },
  ];

  return (
    <div className="min-h-screen bg-linear-to-b from-background to-secondary/10 p-6">
      <div className="mx-auto max-w-7xl">
        {/* Header */}
        <div className="mb-8">
          <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <div className="rounded-lg bg-linear-to-r from-purple-500/10 to-pink-500/10 p-2">
                  <Layout className="h-6 w-6 text-purple-500" />
                </div>
                <h1 className="text-3xl font-bold tracking-tight">Design Templates</h1>
              </div>
              <p className="text-muted-foreground">
                Browse and manage templates for stunning social media designs
              </p>
            </div>
            <Button
              onClick={() => {/* TODO: Add create template flow */ }}
              size="lg"
              className="gap-2 bg-linear-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700"
            >
              <Plus className="h-4 w-4" />
              Create Template
            </Button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="mb-8 grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card className="border-2 border-purple-500/10">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Total Templates</p>
                  <p className="text-3xl font-bold">{templates?.length || 0}</p>
                </div>
                <div className="rounded-lg bg-purple-500/10 p-3">
                  <Layout className="h-6 w-6 text-purple-500" />
                </div>
              </div>
            </CardContent>
          </Card>

          {formatStats.map((stat) => (
            <Card key={stat.format} className="border-2 border-secondary">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-muted-foreground capitalize">
                      {stat.format === 'custom' ? 'Your Templates' : `${stat.format} Format`}
                    </p>
                    <p className="text-3xl font-bold">{stat.count}</p>
                  </div>
                  <div className="rounded-lg bg-secondary p-3">
                    <stat.icon className="h-6 w-6" />
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Main Content Card */}
        <Card className="border-2">
          <CardHeader className="bg-secondary/50 py-6">
            <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
              <div>
                <CardTitle>Template Library</CardTitle>
                <CardDescription>
                  Browse {templates?.length || 0} templates across different formats
                </CardDescription>
              </div>

              {/* Search and Controls */}
              <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
                {/* Search */}
                <div className="relative flex-1 sm:max-w-md">
                  <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                  <Input
                    placeholder="Search templates..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10 border-2"
                  />
                </div>

                {/* View Toggle */}
                <div className="flex items-center gap-2">
                  <div className="flex items-center gap-1 rounded-lg border p-1">
                    <Button
                      size="sm"
                      variant={viewMode === 'grid' ? 'secondary' : 'ghost'}
                      className="h-8 w-8 p-0"
                      onClick={
                        () => handleViewModeChange('grid')
                      }
                    >
                      <Grid3x3 className="h-4 w-4" />
                    </Button>
                    <Button
                      size="sm"
                      variant={viewMode === 'list' ? 'secondary' : 'ghost'}
                      className="h-8 w-8 p-0"
                      onClick={
                        () => handleViewModeChange('list')
                      }
                      disabled
                      title="Coming soon"
                    >
                      <List className="h-4 w-4" />
                    </Button>
                  </div>

                  {/* Filter Menu */}
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="outline" size="icon">
                        <Filter className="h-4 w-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuLabel>Filter Options</DropdownMenuLabel>
                      <DropdownMenuSeparator />
                      <DropdownMenuItem onClick={() => setSelectedFormat('all')}>
                        All Formats
                      </DropdownMenuItem>
                      <DropdownMenuItem onClick={() => setSelectedFormat('square')}>
                        Square (1:1)
                      </DropdownMenuItem>
                      <DropdownMenuItem onClick={() => setSelectedFormat('story')}>
                        Story (9:16)
                      </DropdownMenuItem>
                      <DropdownMenuItem onClick={() => setSelectedFormat('a4')}>
                        A4 Print
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
              </div>
            </div>
          </CardHeader>

          <CardContent className="p-6">
            {/* Format Tabs */}
            <Tabs value={selectedFormat} onValueChange={setSelectedFormat} className="mb-6">
              <TabsList className="grid w-full grid-cols-4 lg:w-auto lg:inline-flex">
                <TabsTrigger value="all" className="gap-2">
                  <Layout className="h-4 w-4" />
                  All
                </TabsTrigger>
                <TabsTrigger value="square" className="gap-2">
                  <Grid3x3 className="h-4 w-4" />
                  Square
                </TabsTrigger>
                <TabsTrigger value="story" className="gap-2">
                  <TrendingUp className="h-4 w-4" />
                  Story
                </TabsTrigger>
                <TabsTrigger value="a4" className="gap-2">
                  <BookOpen className="h-4 w-4" />
                  A4 Print
                </TabsTrigger>
              </TabsList>
            </Tabs>

            {/* Loading State */}
            {isLoading && (
              <div className="space-y-6 py-8">
                <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                  {Array.from({ length: 8 }).map((_, i) => (
                    <div key={i} className="space-y-3">
                      <Skeleton className="h-48 w-full rounded-lg" />
                      <Skeleton className="h-4 w-3/4" />
                      <Skeleton className="h-4 w-1/2" />
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Error State */}
            {isError && (
              <div className="py-12 text-center">
                <div className="rounded-lg border border-destructive/50 bg-destructive/10 p-8">
                  <p className="text-destructive font-semibold">
                    Failed to load templates. Please try again.
                  </p>
                </div>
              </div>
            )}

            {/* Content */}
            <div className="space-y-8">
              {/* System Templates */}
              {!isLoading && systemTemplates.length > 0 && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="rounded-lg bg-linear-to-r from-blue-500/10 to-cyan-500/10 p-2">
                        <Zap className="h-5 w-5 text-blue-500" />
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold">Premium System Templates</h3>
                        <p className="text-sm text-muted-foreground">
                          Professionally designed templates ready to use
                        </p>
                      </div>
                    </div>
                    <Badge variant="outline" className="gap-1">
                      <Sparkles className="h-3 w-3" />
                      {systemTemplates.length} templates
                    </Badge>
                  </div>
                  <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                    {systemTemplates.map((template) => (
                      <TemplateCard
                        key={template.id}
                        template={template}
                        onPreview={handlePreview}
                        onDuplicate={handleDuplicate}
                        viewMode={viewMode}
                      />
                    ))}
                  </div>
                </div>
              )}

              {/* Custom Templates */}
              {!isLoading && customTemplates.length > 0 && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="rounded-lg bg-linear-to-r from-green-500/10 to-emerald-500/10 p-2">
                        <Users className="h-5 w-5 text-green-500" />
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold">Your Custom Templates</h3>
                        <p className="text-sm text-muted-foreground">
                          Templates created and customized by you
                        </p>
                      </div>
                    </div>
                    <Badge variant="secondary" className="gap-1">
                      <Copy className="h-3 w-3" />
                      {customTemplates.length} templates
                    </Badge>
                  </div>
                  <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                    {customTemplates.map((template) => (
                      <TemplateCard
                        key={template.id}
                        template={template}
                        onPreview={handlePreview}
                        onDuplicate={handleDuplicate}
                        onDelete={handleDelete}
                        viewMode={viewMode}
                      />
                    ))}
                  </div>
                </div>
              )}

              {/* Empty State */}
              {!isLoading && filteredTemplates.length === 0 && (
                <div className="py-12">
                  <EmptyState
                    icon={Layout}
                    title={searchQuery ? "No matching templates found" : "No templates yet"}
                    description={
                      searchQuery
                        ? `No templates match "${searchQuery}"`
                        : "Start by exploring system templates or create your own custom design"
                    }
                    action={
                      searchQuery
                        ? {
                          label: 'Clear Search',
                          onClick: () => setSearchQuery(''),
                          variant: 'outline',
                        }
                        : {
                          label: 'Browse System Templates',
                          onClick: () => setSelectedFormat('all'),
                          icon: Sparkles,
                        }
                    }
                  />
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Plan Limit Warning */}
        {!isLoading && plan && customTemplates.length >= plan.max_templates && plan.max_templates !== -1 && (
          <Card className="mt-6 border-2 border-warning">
            <CardContent className="p-6">
              <div className="flex items-start gap-4">
                <div className="rounded-full bg-warning/10 p-2">
                  <Zap className="h-5 w-5 text-warning" />
                </div>
                <div className="flex-1">
                  <h4 className="font-semibold text-warning">Template Limit Reached</h4>
                  <p className="text-sm text-muted-foreground mt-1">
                    You've used all {plan.max_templates} custom templates in your {plan.name} plan.
                    Upgrade to create more custom templates and unlock premium features.
                  </p>
                </div>
                <Button variant="outline" size="sm">
                  Upgrade Plan
                </Button>
              </div>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Enhanced Template Preview Dialog */}
      <TemplatePreviewDialog
        template={previewTemplate}
        open={previewOpen}
        onOpenChange={setPreviewOpen}
        onDuplicate={handleDuplicate}
        onDelete={handleDelete}
      />

      {/* Delete Confirmation Dialog */}
      <AlertDialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <AlertDialogContent className="border-2 border-destructive/20">
          <AlertDialogHeader>
            <div className="flex items-center gap-3">
              <div className="rounded-full bg-destructive/10 p-2">
                <Trash2 className="h-6 w-6 text-destructive" />
              </div>
              <div>
                <AlertDialogTitle>Delete Template</AlertDialogTitle>
                <AlertDialogDescription>
                  This action cannot be undone. This will permanently delete the template
                  and all designs created from it.
                </AlertDialogDescription>
              </div>
            </div>
          </AlertDialogHeader>
          <div className="my-4 rounded-lg bg-secondary/50 p-4">
            <p className="font-semibold">{templateToDelete?.name}</p>
            <div className="mt-2 flex items-center gap-2">
              <Badge variant="outline" className="capitalize">
                {templateToDelete?.format}
              </Badge>
              {templateToDelete?.is_system ? (
                <Badge className="bg-blue-500">System</Badge>
              ) : (
                <Badge variant="secondary">Custom</Badge>
              )}
            </div>
          </div>
          <AlertDialogFooter>
            <AlertDialogCancel variant="outline">Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={confirmDelete}
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            >
              Delete Template
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}