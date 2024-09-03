import { subtitle, title } from "@/components/primitives";

export default function InfoPage() {
  return (
    <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
      <div className="inline-block max-w-lg text-center justify-center">
        <h2 className={subtitle({ class: "mt-4" })}>
          This is a personal project with aims of becoming a data driven news aggregator and tracker to increase transparency and oversight over those with notable political or financial influence.
        </h2>
      </div>
    </ section>
  );
}
