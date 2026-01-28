export interface User {
  id: number;
  user_name: string;
  email: string;
  plan_id: number;
  monthly_generations: number;
  created_at: string;
}

export interface Plan {
  id: number;
  name: string;
  price: number;
  max_products: number;
  max_templates: number;
  monthly_generations: number;
  features: Record<string, boolean>;
}

export interface Product {
  id: number;
  user_id: number;
  name: string;
  price: number;
  category?: string;
  image_url?: string;
  sku?: string;
  description?: string;
  created_at: string;
  updated_at?: string;
}

export interface Template {
  id: number;
  user_id?: number;
  name: string;
  format: 'square' | 'story' | 'a4';
  description?: string;
  background_url?: string;
  json_definition: Record<string, any>;
  preview_url?: string;
  is_system: boolean;
  created_at: string;
  last_used_at?: string;
}

export interface Campaign {
  id: number;
  user_id: number;
  name: string;
  start_date?: string;
  end_date?: string;
  template_id?: number;
  rules: Record<string, any>;
  created_at: string;
}

export interface Poster {
  id: number;
  user_id: number;
  product_id: number;
  campaign_id?: number;
  template_id: number;
  image_url: string;
  format: string;
  status: 'generating' | 'generated' | 'failed';
  created_at: string;
}
