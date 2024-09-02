
export const CVData = {
    personalData: {
      name: 'Jack Gray',
      title: 'Full Stack Data Platform Engineer',
      // image: '',
      contacts: [
        { type: 'email', value: 'contact@jackgray.nyc' },
        { type: 'phone', value: '929-409-5452' },
        { type: 'location', value: 'New York' },
        { type: 'website', value: 'beta-spotlight-us.com' },
        { type: 'linkedin', value: 'linkedin.com/in/johnhgrayiii' },
        // { type: 'twitter', value: 'twitter.com/sbayd' },
        { type: 'github', value: 'github.com/jackgray' }
      ]
    },
    sections: [
      {
        type: 'text',
        title: 'Career Profile',
        content: `**Well-rounded Data/Infrastructure Engineer with a deep expertise in Linux systems, data automation, and modern platform design. While my core strength lies in data and service hosting infrastructure, I\’m also adept at building and deploying full-stack JavaScript applications in production environments.`,
        icon: 'usertie'
      },
      {
        type: 'common-list',
        title: 'Education',
        icon: 'graduation',
        items: [
          {
            title: 'Computer/Electrical Engineering (BS)',
            authority: 'University',
            authorityWebSite: 'https://auburn.edu',
            rightSide: '2009 - 2014'
          },
        ]
      },
      {
        type: 'experiences-list',
        title: 'Experiences',
        description: 'Optional',
        icon: 'archive',
        items: [
          {
            title: 'Head of Data',
            company: 'Brain Research Lab @ Mount Sinai',
            description: `Oversee all data and related technology for 6 active clinical trials and more than 10 prior studies, including compute infrastructure, database modeling/management, ETL/ELT pipelines, and web service development and hosting \
                            Wrangled \> 50TB debt of unstructured text, audio, and neuro-imaging data \
                            Designed  bare metal/cloud hybrid computing cluster and IaC node provisioning using Terraform, Make, Bash, & systemd templates for RHEL CoreOS to produce faster/lighter K8 alternative with low attack surface \
                            Built on-prem tiered distributed object data lake supporting git remotes, container registry, web app storage, databases, large files, ElasticSearch indices, and ETL staging, modernizing data infrastructure while maintaining HIPAA compliance,  high security standards, and scalability \
                            Build batch processing DAG data pipelines in SQL, Bash, and Python, and manage distributed scheduling platform \(Kestra\) \
                            Configure and manage ElasticSearch to load logs, system metrics, and unstructured documents into free-text searchable indices \
                            Automate fMRI processing and time-series alignment of longitudinal data \
                            Model clinical assessment data for relational and graph dbs \
                            Develop and maintain multi-tenant virtual workspace solution offering scalable and portable computing environments with RBAC data access and pre-configured analysis software \
                            Develop and host full stack JavaScript  web applications, enabling daily remote data collection from subject mobile devices, increasing data resolution \
                            Create visual dashboards of data and system metrics in Kibana and Apache Superset`,
            companyWebSite: 'https://beta.spotlight-us.com',
            companyMeta: '',
            datesBetween: '2017.10 - Present',
            descriptionTags: ['Javascript', 'React']
          },
          {
            title: 'Software Developer',
            company: 'Some Company Example INC',
            description: 'I\'m using ReactJS and working as a front-end developer',
            companyWebSite: 'http://somecompanyexample.com',
            companyMeta: 'Little info about company',
            datesBetween: '2016.8 - 2017.10'
          },
          {
            title: 'Intern',
            company: 'Some Software Example INC',
            description: 'I was warming up.',
            companyWebSite: 'http://someexamplecompany.com',
            companyMeta: 'SF USA',
            datesBetween: '2012.06 - 2012.10'
          }
        ]
      },
      {
        type: 'projects-list',
        title: 'Projects',
        description: 'Optional',
        icon: 'tasks',
        groups: [
          {
            sectionHeader: 'Company Name',
            description: 'Optional',
            items: [
              { title: 'Project', projectUrl: 'optional', description: 'Optional' },
              { title: 'Project', projectUrl: 'optional', description: 'Optional' },
              { title: 'Project', projectUrl: 'optional', description: 'Optional' }
            ]
          }
        ]
      },
      {
        type: 'common-list',
        title: 'Conferences & Certificates',
        description: '',
        icon: 'comments',
        items: [
          {
            title: 'Some Conferences / 2019',
            authority: 'SomeConf',
            authorityWebSite: 'https://www.someconf.somesome'
          },
          {
            title: 'Some Conferences / 2019',
            authority: 'SomeConf',
            authorityMeta: 'Speaker',
            authorityWebSite: 'https://www.someconf.somesome',
            rightSide: 'test'
          },
          {
            title: 'Some Conferences / 2012',
            authorityMeta: 'Speaker'
          }
        ]
      },
      {
        type: 'common-list',
        title: 'Languages',
        icon: 'language',
        items: [
          {
            authority: 'English',
            authorityMeta: 'Professional'
          },
          {
            authority: 'Spanish',
            authorityMeta: 'Beginner'
          }
        ]
      },
      {
        type: 'tag-list',
        title: 'Skills Proficiency',
        icon: 'rocket',
        items: ['React', 'Javascript', 'CSS', 'SQL', 'SomeTech', 'CoolTech']
      },
      {
        type: 'tag-list',
        title: 'Hobbies & Interests',
        icon: 'cubes',
        items: ['Photography', 'Poetry']
      }
    ]
  }