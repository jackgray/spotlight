import { title, subtitle } from "@/components/primitives";
import DescriptionBox from '@/components/DescriptionBox';


export default function Home() {

  return (
    <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
      <div className="inline-block max-w-lg text-center justify-center">
        {/* <h1 className={title()}>Keep a &nbsp;</h1>
        <h1 className={title({ color: "violet" })}>SPOTLIGHT&nbsp;</h1>
        <br />
        <h1 className={title()}>
          on abuse of power.
        </h1>
        <h2 className={subtitle({ class: "mt-4" })}>
          With data driven reporting.
        </h2> */}
        <h1 className={title()}>Aggregated data from hard to reach places</h1>
  
        <h2 className={`${subtitle()} mt-4`}>
          Spotlight is a generalized data aggregator and distribution platform. It aims to support data driven journalism and encourage civic engagement. The goal is to provide a scalable framework for easily adding data scraping pipelines. Start by exploring the Finance / Wall St. page -- this is where Spotlight&apos;s efforts are currently directed. Interact with the charts, or export the data to Excel or CSV by clicking the context menu of a chart.
        </h2>
        
        <div className='mt-4'>
          <DescriptionBox label='Construction notice' text="Note that many of the links on this site are inactive or may not behave properly. I am making them publicly visible to show what I hope this site will become." />
        </div>
      </div>

      {/* <div className="flex gap-3">
        <Link
          isExternal
          className={buttonStyles({
            color: "primary",
            radius: "full",
            variant: "shadow",
          })}
          href={siteConfig.links.docs}
        >
          Documentation
        </Link>
        <Link
          isExternal
          className={buttonStyles({ variant: "bordered", radius: "full" })}
          href={siteConfig.links.github}
        >
          <GithubIcon size={20} />
          GitHub
        </Link>
      </div> */}

      {/* <div className="mt-8">
        <Snippet hideCopyButton hideSymbol variant="bordered">
          <span>
            Get started by editing <Code color="primary">app/page.tsx</Code>
          </span>
        </Snippet>
      </div> */}
    </section>
  );
}
