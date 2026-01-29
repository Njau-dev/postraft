'use client';

import { Template } from '@/types';
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import {
  Copy,
  Edit,
  MoreVertical,
  Trash2,
  Eye,
  Sparkles,
  Zap,
  Layers,
  Ruler,
  Download,
  Star,
  Share2,
  Play
} from 'lucide-react';
import Image from 'next/image';

interface TemplateCardProps {
  template: Template;
  onPreview: (template: Template) => void;
  onDuplicate: (template: Template) => void;
  onEdit?: (template: Template) => void;
  onDelete?: (template: Template) => void;
  viewMode?: 'grid' | 'list';
}

export default function TemplateCard({
  template,
  onPreview,
  onDuplicate,
  onEdit,
  onDelete,
  viewMode = 'grid',
}: TemplateCardProps) {
  const canEdit = !template.is_system;

  const getFormatColor = () => {
    switch (template.format) {
      case 'square': return 'bg-green-500/10 text-green-600 border-green-500/20';
      case 'story': return 'bg-purple-500/10 text-purple-600 border-purple-500/20';
      case 'a4': return 'bg-blue-500/10 text-blue-600 border-blue-500/20';
      default: return 'bg-secondary text-secondary-foreground';
    }
  };

  const getFormatIcon = () => {
    switch (template.format) {
      case 'square': return '▢';
      case 'story': return '📱';
      case 'a4': return '📄';
      default: return '🎨';
    }
  };

  const getLayerCount = () => {
    return template.json_definition?.layers?.length || 0;
  };

  console.log('View mode on card:', viewMode);

  const getPopularityBadge = () => {
    // Mock popularity based on template ID or last_used_at
    const lastUsed = template.last_used_at ? new Date(template.last_used_at) : null;
    const daysSinceUse = lastUsed ? (new Date().getTime() - lastUsed.getTime()) / (1000 * 3600 * 24) : Infinity;

    if (daysSinceUse < 7) return { text: 'Trending', color: 'bg-orange-500' };
    if (template.is_system) return { text: 'Popular', color: 'bg-blue-500' };
    return null;
  };

  const popularity = getPopularityBadge();

  if (viewMode === 'list') {
    return (
      <Card className="group overflow-hidden border-2 transition-all hover:border-primary/20 hover:shadow-lg">
        <div className="flex items-stretch">
          {/* Preview */}
          <div
            className="relative w-32 cursor-pointer overflow-hidden bg-linear-to-br from-primary/5 to-primary/20 md:w-48"
            onClick={() => onPreview(template)}
          >
            {template.preview_url ? (
              <Image
                src={template.preview_url}
                alt={template.name}
                fill
                className="object-cover transition-transform group-hover:scale-105"
                sizes="192px"
              />
            ) : (
              <div className="flex h-full items-center justify-center">
                <div className="text-center">
                  <div className="mx-auto mb-2 rounded-full bg-secondary p-3">
                    <Sparkles className="h-6 w-6 text-muted-foreground" />
                  </div>
                  <p className="text-xs text-muted-foreground">No preview</p>
                </div>
              </div>
            )}
          </div>

          {/* Content */}
          <div className="flex flex-1 flex-col p-4">
            <div className="flex items-start justify-between">
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <h3 className="font-semibold">{template.name}</h3>
                  {popularity && (
                    <Badge className={`${popularity.color} text-white`}>
                      {popularity.text}
                    </Badge>
                  )}
                </div>
                <p className="text-sm text-muted-foreground line-clamp-2">
                  {template.description || 'No description provided'}
                </p>
              </div>

              <div className="flex items-center gap-2">
                <Badge
                  variant="outline"
                  className={`${getFormatColor()} gap-1`}
                >
                  <span className="text-sm">{getFormatIcon()}</span>
                  <span className="capitalize">{template.format}</span>
                </Badge>
                {template.is_system && (
                  <Badge className="gap-1 bg-linear-to-r from-blue-500 to-cyan-500">
                    <Zap className="h-3 w-3" />
                    System
                  </Badge>
                )}
              </div>
            </div>

            <div className="mt-4 flex flex-1 items-end justify-between">
              <div className="flex items-center gap-4 text-sm text-muted-foreground">
                <div className="flex items-center gap-1">
                  <Layers className="h-4 w-4" />
                  <span>{getLayerCount()} layers</span>
                </div>
                <div className="flex items-center gap-1">
                  <Ruler className="h-4 w-4" />
                  <span>
                    {template.json_definition?.canvas?.w || 0}×{template.json_definition?.canvas?.h || 0}
                  </span>
                </div>
                {template.last_used_at && (
                  <div className="hidden md:block">
                    Last used: {new Date(template.last_used_at).toLocaleDateString()}
                  </div>
                )}
              </div>

              <div className="flex items-center gap-2">
                <Button
                  size="sm"
                  variant="outline"
                  className="gap-2"
                  onClick={() => onDuplicate(template)}
                >
                  <Copy className="h-4 w-4" />
                  Duplicate
                </Button>
                <Button
                  size="sm"
                  className="gap-2"
                  onClick={() => onPreview(template)}
                >
                  <Play className="h-4 w-4" />
                  Use Template
                </Button>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button size="icon" variant="ghost">
                      <MoreVertical className="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuLabel>Actions</DropdownMenuLabel>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem onClick={() => onPreview(template)}>
                      <Eye className="mr-2 h-4 w-4" />
                      Preview
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => onDuplicate(template)}>
                      <Copy className="mr-2 h-4 w-4" />
                      Duplicate
                    </DropdownMenuItem>
                    {onEdit && canEdit && (
                      <DropdownMenuItem onClick={() => onEdit(template)}>
                        <Edit className="mr-2 h-4 w-4" />
                        Edit
                      </DropdownMenuItem>
                    )}
                    <DropdownMenuItem>
                      <Download className="mr-2 h-4 w-4" />
                      Export
                    </DropdownMenuItem>
                    <DropdownMenuItem>
                      <Share2 className="mr-2 h-4 w-4" />
                      Share
                    </DropdownMenuItem>
                    {onDelete && canEdit && (
                      <>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem
                          onClick={() => onDelete(template)}
                          className="text-destructive"
                        >
                          <Trash2 className="mr-2 h-4 w-4" />
                          Delete
                        </DropdownMenuItem>
                      </>
                    )}
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            </div>
          </div>
        </div>
      </Card>
    );
  }

  // Grid View (default)
  return (
    <Card className="group relative h-full overflow-hidden border-2 transition-all hover:border-primary/20 hover:shadow-xl">
      {/* Popularity Badge */}
      {popularity && (
        <div className="absolute left-3 top-3 z-10">
          <Badge className={`${popularity.color} gap-1 text-white`}>
            <Star className="h-3 w-3 fill-current" />
            {popularity.text}
          </Badge>
        </div>
      )}

      {/* Template Preview */}
      <CardHeader className="p-0">
        <div
          className="relative aspect-square cursor-pointer overflow-hidden bg-linear-to-br from-primary/5 to-primary/20"
          onClick={() => onPreview(template)}
        >
          {template.preview_url ? (
            <>
              <Image
                src={template.preview_url}
                alt={template.name}
                fill
                className="object-cover transition-transform duration-300 group-hover:scale-110"
                sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
              />
              {/* Gradient Overlay */}
              <div className="absolute inset-0 bg-linear-to-t from-black/60 via-transparent to-transparent opacity-0 transition-opacity group-hover:opacity-100" />
            </>
          ) : (
            <div className="flex h-full flex-col items-center justify-center p-6">
              <div className="mb-4 rounded-full bg-linear-to-r from-purple-500/10 to-pink-500/10 p-4">
                <Sparkles className="h-8 w-8 text-muted-foreground" />
              </div>
              <p className="text-sm text-muted-foreground">No preview available</p>
            </div>
          )}

          {/* Format Badge */}
          <div className="absolute right-3 top-3">
            <Badge
              variant="outline"
              className={`${getFormatColor()} gap-1 backdrop-blur-sm`}
            >
              <span className="text-sm">{getFormatIcon()}</span>
              <span className="hidden capitalize sm:inline">{template.format}</span>
            </Badge>
          </div>

          {/* System Badge */}
          {template.is_system && (
            <div className="absolute left-3 bottom-3">
              <Badge className="gap-1 bg-linear-to-r from-blue-500 to-cyan-500">
                <Zap className="h-3 w-3" />
                System
              </Badge>
            </div>
          )}

          {/* Hover Overlay Actions */}
          <div className="absolute inset-0 flex items-center justify-center bg-black/70 opacity-0 transition-all duration-300 group-hover:opacity-100">
            <div className="flex flex-col gap-3 p-4">
              <Button
                size="lg"
                className="gap-2"
                onClick={(e) => {
                  e.stopPropagation();
                  onPreview(template);
                }}
              >
                <Eye className="h-5 w-5" />
                Quick Preview
              </Button>
              <div className="grid grid-cols-2 gap-2">
                <Button
                  variant="secondary"
                  size="sm"
                  className="gap-2"
                  onClick={(e) => {
                    e.stopPropagation();
                    onDuplicate(template);
                  }}
                >
                  <Copy className="h-4 w-4" />
                  Duplicate
                </Button>
                <Button
                  variant="secondary"
                  size="sm"
                  className="gap-2"
                  onClick={(e) => {
                    e.stopPropagation();
                    // TODO: Implement quick use
                    console.log('Quick use template:', template);
                  }}
                >
                  <Play className="h-4 w-4" />
                  Use Now
                </Button>
              </div>
            </div>
          </div>
        </div>
      </CardHeader>

      {/* Template Info */}
      <CardContent className="p-4">
        <div className="space-y-2">
          <div className="flex items-start justify-between">
            <h3 className="line-clamp-1 font-semibold">{template.name}</h3>
            <div className="flex items-center gap-1 text-sm text-muted-foreground">
              <Layers className="h-4 w-4" />
              <span>{getLayerCount()}</span>
            </div>
          </div>
          <p className="line-clamp-2 text-sm text-muted-foreground">
            {template.description || 'No description provided'}
          </p>
          <div className="flex items-center justify-between text-xs text-muted-foreground">
            <div className="flex items-center gap-1">
              <Ruler className="h-3 w-3" />
              <span>
                {template.json_definition?.canvas?.w || 0}×{template.json_definition?.canvas?.h || 0}
              </span>
            </div>
            {template.last_used_at && (
              <span>Used {new Date(template.last_used_at).toLocaleDateString()}</span>
            )}
          </div>
        </div>
      </CardContent>

      {/* Actions Footer */}
      <CardFooter className="flex gap-2 p-4 pt-0">
        <Button
          variant="outline"
          className="flex-1 gap-2"
          size="sm"
          onClick={() => onDuplicate(template)}
        >
          <Copy className="h-4 w-4" />
          Duplicate
        </Button>

        <Button
          className="flex-1 gap-2"
          size="sm"
          onClick={() => onPreview(template)}
        >
          <Eye className="h-4 w-4" />
          Preview
        </Button>

        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button size="icon" variant="ghost" className="h-10 w-10">
              <MoreVertical className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-48">
            <DropdownMenuLabel>More Actions</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={() => onDuplicate(template)}>
              <Copy className="mr-2 h-4 w-4" />
              Duplicate Template
            </DropdownMenuItem>
            {onEdit && canEdit && (
              <DropdownMenuItem onClick={() => onEdit(template)}>
                <Edit className="mr-2 h-4 w-4" />
                Edit Template
              </DropdownMenuItem>
            )}
            <DropdownMenuItem onClick={() => onPreview(template)}>
              <Eye className="mr-2 h-4 w-4" />
              Full Preview
            </DropdownMenuItem>
            <DropdownMenuItem>
              <Download className="mr-2 h-4 w-4" />
              Export JSON
            </DropdownMenuItem>
            <DropdownMenuItem>
              <Share2 className="mr-2 h-4 w-4" />
              Share Template
            </DropdownMenuItem>
            {onDelete && canEdit && (
              <>
                <DropdownMenuSeparator />
                <DropdownMenuItem
                  onClick={() => onDelete(template)}
                  className="text-destructive"
                >
                  <Trash2 className="mr-2 h-4 w-4" />
                  Delete Template
                </DropdownMenuItem>
              </>
            )}
          </DropdownMenuContent>
        </DropdownMenu>
      </CardFooter>
    </Card>
  );
}