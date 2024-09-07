import { subtitle, title } from "@/components/primitives";

export default function InfoPage() {
  return (
    <>
      <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
        <div className="inline-block max-w-lg text-center justify-center">
          <h2 className={subtitle({ class: "mt-4" })}>
            Hi, and welcome to the preview of Spotlight! All around us decisions are being made behind closed doors that affect so many aspects of our lives in ways we can&apos;t see or trace, from healthcare access and legislation to global economy. 
            When no one is watching, people have a tendency to behave more selfishly. When activities are transparent, and people can put a name and face to an event, there is better incentive to act in the interests of the populace.
          </h2>
          <h2 className={subtitle({ class: "mt-4" })}>
            Properly curated data has the power to drive this effect. That is the goal of Spotlight--to be a resource to journalists and researchers, and encourage engagement from everyday citizens through ease of access and use.
          </h2>
          <h2 className={subtitle({ class: "mt-4" })}>
            Dealings which are supposed to represent the interest of the people, or risk economic health and result in taxpayer bail-outs should not be made in the shadows. This project attempts to point a spotlight on those dealings, and hopes to be a platform where anyone can spectate without having to be an expert or wrangle data from a handful of regulatory agencies to get the full picture.
          </h2>
          <h2 className={subtitle({ class: "mt-4" })}>
            In alignment with Spotlight&apos;s spirit of transparency and open-data, it&apos;s an open-source project, and you can inspect and contribute to the code used to source the data it provides in its GitHub project. Contact me at contact@jackgray.nyc if you want to know what I need help with the most, or simply make a pull request on the GitHub project.
          </h2>
        </div>
      </ section>
    </>
  );
}
