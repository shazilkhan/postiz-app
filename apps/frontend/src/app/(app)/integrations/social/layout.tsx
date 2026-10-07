import { ReactNode } from 'react';

export default async function IntegrationLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <div className="bg-[#0A0908] flex flex-1 min-h-screen w-screen">
      {children}
    </div>
  );
}
