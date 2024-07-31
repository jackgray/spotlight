# Kafka Producer Library

This directory contains a set of Kafka producers that can run in a DAG scheduler or standalone docker container managed by your container run environment

They are composed primarily of two components: protobuf data conversion, which formats the data in probably the most efficient format available for Kafka streaming, and Kafka producers which send the serialized data to the Kafka broker hosting topics which receive them

## swaps

Pulls zipped csv files for a range of dates from the DTCC. Traditionally, a single zip file containing a single csv must be downloaded each day. This package aims to automate that task and allow automated retreival of new data

More info about where swap contracts are reported to below

# Change Data Capture

It's important not to make exessive API calls and request data that has already been ingested.

This can pose several challenges in highly decoupled applications where Kafka is mostly an upstream processor.

## Using unique producer generated IDs
if the payload includes a unique id composed of concatenated strings from the result of the request, this id can be stored by the kafka queue to track what has already been sent and prevent redundant requests


# SWAP DATA REPOSITORIES

When a swap agreement is made, the transaction must be filed with qualifying swap data repository (SDR)

The nature of the swap and underlying assets determine which agencies a party has the option of filing with. 

CME Group

CFTC - If the traded assets are large index funds like the SPY, or a commodity like silver or steel. It is possible for a commodity and an equity such as stock or options contract to get put in the same basket, and *I believe* the requirement is that this is filed with EACH of the relevant parties, so in this case the swap would also be filed to the SEC via DTCC as well as CFTC. I have nothing to back this up with though, as I'm still investigating.

ICE - ICE is a private company and qualified SDR. Their main selling point is anonymnity, so their reports don't contain as much information, and some data is restricted to parties not involved in the deal. See section below on ICE data

DTCC - DTCC hosts datasets for both CFTC and SEC filed swaps

The fact that coorporations have been caught in the past funneling swaps through as many as 35 shell companies


https://www.cftc.gov/sites/default/files/idc/groups/public/@newsroom/documents/file/fd_factsheet_final.pdf

https://www.cftc.gov/sites/default/files/About/Economic%20Analysis/Introducing%20ENNs%20v4.pdf

#### Definition of “Swap” and “Security-Based Swap”
The Commissions believe that the definitions of “swap” and “security-based swap” in Title VII are detailed and comprehensive. However, as the Commissions did in the Proposing Release, the Commissions are clarifying in the final rules and interpretations that certain insurance products, consumer and commercial agreements, and loan participations are not swaps or security-based swaps.


#### DTCC Data

The DTCC offers datasets submitted to both SEC and CFTC

https://pddata.dtcc.com/ppd/

https://kgc0418-tdw-data-3.s3.amazonaws.com/gtr/static/gtr/docs/RT_PPD_quick_ref_guide.pdf

#### ICE Data

https://ir.theice.com/press/news-details/2021/ICE-Announces-that-ICE-Trade-Vault-is-Approved-by-the-SEC-as-a-Security-Based-Swap-Data-Repository/default.aspx

https://www.ice.com/swap-trade/regulation

Market Supervision
ICE Swap Trade is responsible for the management, monitoring and regulation of all trading activity for CFTC regulated products. All market activity is monitored by our team that provides front-line trading and back office support.

##### Access
https://www.sec.gov/files/rules/other/2021/ice-trade-vault/exhibit-v.2-ice-trade-vault-disclosure-document-feb-2021.pdf

Access to and usage of the ICE SBSDR Service is available to all market participants that validly engage in Security-based swap transactions and to all market venues from which data can be submitted to the ICE SBSDR Service. Access to and use of the ICE SBSDR Service does not require the use of any other ancillary service offered by ICE Trade Vault.

For security reasons, *access to the ICE Trade Vault system is strictly limited to entities with valid permissions and security access (“Users”), Regulators and the U.S. Securities and Exchange Commission (the “SEC”). Users will only have access to (i) data they reported, (ii) data that pertains to a Security-based swap to which they are a Counterparty; (iii) data that pertains to a Security - based swap for which the User is an Execution Agent, Platform, registered broker-dealer or a Third-Party Reporter; and (iv) data that ICE Trade Vault is required to make publicly available.* Passwords must meet technical and procedural processes for information security and must include at least three of the following elements: uppercase letters, lowercase letters, numbers, special characters.

###### User Access Criteria
Access to the ICE SBSDR Service is provided to Users that have duly executed a User Agreement with ICE Trade Vault and have completed and delivered to ICE Trade Vault the applicable ICE Trade Vault enrollment forms.Thes edocuments are available upon request from ICE Trade Vault.

 When enrolling with ICE Trade Vault, Users must designate a master user ("Administrator"). The Administrator will create, permission and maintain all user names and passwords for its f irm. This ensures ICE Trade Vault access is granted by a trusted individual at the User’s firm who is closest to and has the most knowledge of those in the firm who require access.
ICE Trade Vault may decline the request of an applicant to become a User of the ICE SBSDR Service if such denial is required in order to comply with Applicable Law (e.g., to comply with sanctions administered and enforced by the Office of Foreign Assets Control of the U.S. Department of the Treasury (“OFAC”)).

If an applicant is denied by ICE Trade Vault for any other reason, the applicant will be entitled to notice and an opportunity to contest such determination in accordance with the Rulebook. If the denial of an application is reversed, the applicant will be granted access to the ICE SBSDR Service promptly following completion of onboarding requirements.


### SWAPs: packaging 'meme' stocks up into toxic debt bundles. It's 2008 all over again!
https://www.sec.gov/comments/s7-10-21/s71021-9177172-248310.pdf


https://www.reddit.com/r/Superstonk/comments/1d2l85e/all_equity_swaps_data_since_21422_source_download/?share_id=9H4_VaON_J2TRJyj57w5-&utm_content=2&utm_medium=ios_app&utm_name=ioscss&utm_source=share&utm_term=1