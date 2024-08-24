export default function DataLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <section className="py-8 md:py-10">
        {children}
    </section>
  );
}
