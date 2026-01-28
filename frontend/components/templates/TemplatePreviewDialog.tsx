'use client';

import { Template } from '@/types';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  Copy,
  Eye,
  Layers,
  Image as ImageIcon,
  Type,
  Box,
  Palette,
  Ruler,
  Download,
  Share2,
  Sparkles,
  Zap,
  Trash2,
  MoreHorizontal
} from 'lucide-react';
import Image from 'next/image';

interface TemplatePreviewDialogProps {
  template: Template | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onDuplicate: (template: Template) => void;
  onDelete?: (template: Template) => void;
}

export default function TemplatePreviewDialog({
  template,
  open,
  onOpenChange,
  onDuplicate,
  onDelete,
}: TemplatePreviewDialogProps) {
  if (!template) return null;

  const layers = template.json_definition?.layers || [];
  const canvas = template.json_definition?.canvas || { w: 0, h: 0 };

  const getLayerIcon = (type: string) => {
    switch (type) {
      case 'image': return <ImageIcon className="h-4 w-4" />;
      case 'text': return <Type className="h-4 w-4" />;
      case 'shape': return <Box className="h-4 w-4" />;
      default: return <Layers className="h-4 w-4" />;
    }
  };

  const formatDimensions = (w: number, h: number) => {
    const aspectRatio = w / h;
    let ratio = '';
    if (Math.abs(aspectRatio - 1) < 0.01) ratio = ' (1:1)';
    else if (Math.abs(aspectRatio - 9 / 16) < 0.01) ratio = ' (9:16)';
    else if (Math.abs(aspectRatio - 16 / 9) < 0.01) ratio = ' (16:9)';
    return `${w} × ${h}px${ratio}`;
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="min-w-6xl max-h-[95vh] border-2 border-primary/20">
        <DialogHeader>
          <div className="flex items-start justify-between">
            <div className="space-y-2">
              <div className="flex items-center gap-3">
                <div className="rounded-lg bg-linear-to-r from-purple-500/10 to-pink-500/10 p-2">
                  {template.is_system ? (
                    <Zap className="h-6 w-6 text-purple-500" />
                  ) : (
                    <Sparkles className="h-6 w-6 text-pink-500" />
                  )}
                </div>
                <div>
                  <DialogTitle className="text-2xl">{template.name}</DialogTitle>
                  <DialogDescription>
                    {template.description || 'No description provided'}
                  </DialogDescription>
                </div>
              </div>
            </div>
            <div className="flex gap-2">
              <Badge variant="outline" className="gap-1 capitalize">
                <Ruler className="h-3 w-3" />
                {template.format}
              </Badge>
              {template.is_system ? (
                <Badge className="gap-1 bg-linear-to-r from-blue-500 to-cyan-500">
                  <Zap className="h-3 w-3" />
                  System
                </Badge>
              ) : (
                <Badge variant="secondary" className="gap-1">
                  <Sparkles className="h-3 w-3" />
                  Custom
                </Badge>
              )}
            </div>
          </div>
        </DialogHeader>

        <div className="grid gap-6 lg:grid-cols-3">
          {/* Left Column: Preview */}
          <div className="lg:col-span-2">
            <Card className="border-2">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Eye className="h-5 w-5" />
                  Preview
                </CardTitle>
                <CardDescription>
                  Template dimensions: {formatDimensions(canvas.w, canvas.h)}
                </CardDescription>
              </CardHeader>
              <CardContent>
                {template.preview_url ? (
                  <div className="relative aspect-square w-full overflow-hidden rounded-lg border-2 bg-linear-to-br from-secondary/50 to-background">
                    <Image
                      src={template.preview_url}
                      alt={template.name}
                      fill
                      className="object-contain p-4"
                      sizes="(max-width: 768px) 100vw, 66vw"
                    />
                  </div>
                ) : (
                  <div className="flex aspect-square items-center justify-center rounded-lg border-2 border-dashed bg-secondary/50">
                    <div className="text-center">
                      <ImageIcon className="mx-auto h-12 w-12 text-muted-foreground" />
                      <p className="mt-2 text-sm text-muted-foreground">No preview available</p>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Right Column: Details & Actions */}
          <div className="space-y-6">
            {/* Quick Actions Card */}
            <Card className="border-2">
              <CardHeader>
                <CardTitle className="text-lg">Quick Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button
                  className="w-full gap-2"
                  onClick={() => {
                    onDuplicate(template);
                    onOpenChange(false);
                  }}
                >
                  <Copy className="h-4 w-4" />
                  Duplicate & Customize
                </Button>
                <div className="grid grid-cols-2 gap-2">
                  <Button variant="outline" className="gap-2">
                    <Download className="h-4 w-4" />
                    Export
                  </Button>
                  <Button variant="outline" className="gap-2">
                    <Share2 className="h-4 w-4" />
                    Share
                  </Button>
                </div>
                {onDelete && !template.is_system && (
                  <Button
                    variant="destructive"
                    className="w-full gap-2"
                    onClick={() => {
                      onDelete(template);
                      onOpenChange(false);
                    }}
                  >
                    <Trash2 className="h-4 w-4" />
                    Delete Template
                  </Button>
                )}
              </CardContent>
            </Card>

            {/* Template Details Card */}
            <Card className="border-2">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Layers className="h-5 w-5" />
                  Template Details
                </CardTitle>
              </CardHeader>
              <CardContent>
                <Tabs defaultValue="layers">
                  <TabsList className="grid w-full grid-cols-2">
                    <TabsTrigger value="layers">Layers ({layers.length})</TabsTrigger>
                    <TabsTrigger value="info">Info</TabsTrigger>
                  </TabsList>

                  <TabsContent value="layers" className="mt-4 space-y-2">
                    {layers.map((layer: any, index: number) => (
                      <div
                        key={index}
                        className="flex items-center justify-between rounded-lg border p-3 hover:bg-secondary/50"
                      >
                        <div className="flex items-center gap-3">
                          <div className="rounded-md bg-primary/10 p-2">
                            {getLayerIcon(layer.type)}
                          </div>
                          <div>
                            <p className="text-sm font-medium capitalize">{layer.type} Layer</p>
                            {layer.key && (
                              <p className="text-xs text-muted-foreground">{layer.key}</p>
                            )}
                          </div>
                        </div>
                        <Badge variant="outline" className="text-xs">
                          #{index + 1}
                        </Badge>
                      </div>
                    ))}
                  </TabsContent>

                  <TabsContent value="info" className="mt-4 space-y-4">
                    <div>
                      <h4 className="text-sm font-medium mb-2">Canvas Properties</h4>
                      <div className="space-y-1 text-sm">
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">Width:</span>
                          <span className="font-medium">{canvas.w}px</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">Height:</span>
                          <span className="font-medium">{canvas.h}px</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">Format:</span>
                          <Badge variant="outline" className="capitalize">
                            {template.format}
                          </Badge>
                        </div>
                      </div>
                    </div>

                    <Separator />

                    <div>
                      <h4 className="text-sm font-medium mb-2">Usage</h4>
                      <div className="space-y-1 text-sm">
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">Created:</span>
                          <span className="font-medium">
                            {new Date(template.created_at).toLocaleDateString()}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">Last Used:</span>
                          <span className="font-medium">
                            {template.last_used_at
                              ? new Date(template.last_used_at).toLocaleDateString()
                              : 'Never'}
                          </span>
                        </div>
                      </div>
                    </div>
                  </TabsContent>
                </Tabs>
              </CardContent>
            </Card>

            {/* Color Palette Card (if available) */}
            {template.json_definition?.colors && (
              <Card className="border-2">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Palette className="h-5 w-5" />
                    Color Palette
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    {Object.entries(template.json_definition.colors).map(([name, color]) => (
                      <div key={name} className="flex flex-col items-center">
                        <div
                          className="h-8 w-8 rounded-full border"
                          style={{ backgroundColor: color as string }}
                        />
                        <span className="mt-1 text-xs capitalize">{name}</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>

        {/* Footer Actions */}
        <div className="flex justify-between border-t pt-4">
          <Button
            variant="ghost"
            onClick={() => onOpenChange(false)}
          >
            Close Preview
          </Button>
          <div className="flex gap-2">
            <Button
              variant="outline"
              onClick={() => {
                // TODO: Implement use in design
                console.log('Use template:', template);
              }}
            >
              Use in Design
            </Button>
            <Button
              onClick={() => {
                onDuplicate(template);
                onOpenChange(false);
              }}
              className="gap-2 bg-linear-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700"
            >
              <Copy className="h-4 w-4" />
              Duplicate & Edit
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}