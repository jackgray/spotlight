export default function ResumeLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <main className="container mx-auto max-w-full pt-1 px-1 flex-grow">
      {children}
    </main>
  );
}
