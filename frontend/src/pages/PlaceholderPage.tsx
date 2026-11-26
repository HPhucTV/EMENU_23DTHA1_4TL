import { Link } from 'react-router-dom';

interface PlaceholderPageProps {
  title: string;
  storyRef: string;
  description: string;
}

export function PlaceholderPage({ title, storyRef, description }: PlaceholderPageProps) {
  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 py-16">
      <div className="rounded-2xl bg-white border border-stone-200 p-8 space-y-4">
        <span className="inline-block rounded-full bg-brand-soft px-3 py-1 text-xs font-semibold text-brand">
          Khung điều hướng sẵn sàng • {storyRef}
        </span>
        <h1 className="font-serif text-3xl sm:text-4xl font-semibold text-stone-900">{title}</h1>
        <p className="text-stone-600 leading-relaxed">{description}</p>
        <div className="pt-2">
          <Link
            to="/"
            className="inline-flex items-center gap-2 rounded-lg bg-brand px-4 py-2.5 text-sm font-medium text-white hover:bg-brand-dark transition-colors"
          >
            ← Quay về Trang chủ
          </Link>
        </div>
      </div>
    </div>
  );
}
