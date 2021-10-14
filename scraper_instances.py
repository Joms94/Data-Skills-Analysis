'''
Contains instances of the scraper class to be used with various job sites.
'''
from scraper_class import Scraper


postjobfree_scraper = Scraper(
                        url_to_scrape='https://www.postjobfree.com/jobs?q=%22Data+Analyst%22&l=Australia',
                        page_results_xpath='/html/body/div/div[@class="stdContentLayout innercontent"]/table/tbody/tr/td[@style="text-align:right;"]',
                        content_xpath='/html/body/div/div[@class="stdContentLayout innercontent"]/div[@style="overflow-wrap:break-word;"]/div[@class="snippetPadding"][{}]/h3[@class="itemTitle"]/a',
                        jobtitle_html='/html/body/div[1]/div[2]/div[1]/div[3]/h1',
                        company_html='/html/body/div[1]/div[2]/div[1]/div[4]/span[1]/span',
                        location_html='/html/body/div[1]/div[2]/div[1]/div[4]/a',
                        posted_html='/html/body/div[1]/div[2]/div[1]/div[4]/span[2]',
                        body_html='/html/body/div[1]/div[2]/div[1]/div[5]/div[2]',
                        salary_html='/html/body/div[1]/div[2]/div[1]/div[4]/div[3]',
                        page_turn_xpath='/html/body/div/div[@class="stdContentLayout innercontent"]/div[@style="text-align:center;padding-top:15px; margin:5px;font-size:large;"]/a[text()[contains(., "Next")]]',
                        result_count='/html/body/div/div[2]/div[2]/div')


jobserve_scraper = Scraper(
                        url_to_scrape='https://www.jobserve.com/au/en/JobListing.aspx?shid=E07150625B7AE5D9BF0B',
                        page_results_xpath='/html/body/form/div[4]/div[1]/div[4]/div[2]/div[3]/div[5]/div[1]/h4[1]/span[1]',
                        content_xpath='/html/body/form/div[4]/div[1]/div[4]/div[2]/div[3]/div[5]/div[2]/div/div[1]/div[5]/div/div[{}]/div[1]/a',
                        jobtitle_html='/html/body/form/div[4]/div[1]/div[6]/div[1]/div[2]/div/div/div[@class="top_detail"]/div[1]/h1/div',
                        company_html='/html/body/form/div[4]/div[1]/div[6]/div[1]/div[2]/div/div/div[@class="top_detail"]/div[1]/span[3]',
                        location_html='/html/body/form/div[4]/div[1]/div[6]/div[1]/div[2]/div/div/div[@class="top_detail"]/div[1]/span[1]',
                        posted_html='/html/body/form/div[4]/div[1]/div[6]/div[1]/div[2]/div/div/div[@class="top_detail"]/div[1]/span[4]',
                        body_html='/html/body/form/div[4]/div[1]/div[6]/div[1]/div[2]/div/div/div[@id="JobDetailContainer"]/div/div/div[1]/div/div[@class="main_detail_content"]/div[@id="md_skills"]',
                        salary_html='/html/body/form/div[4]/div[1]/div[6]/div[1]/div[2]/div/div/div[4]/div/div/div[1]/div/div/div[9]/div[6]/span',
                        page_turn_xpath='/html/body/form/div[4]/div[1]/div[4]/div[2]/div[3]/div[5]/div[2]/div/div[1]/div[6]/div/span[@class="nav_Next"]/a/img',
                        result_count='/html/body/form/div[4]/div[1]/div[4]/div[2]/div[3]/div[5]/div[2]/div/div[1]/div[5]/div/div')


if __name__ == '__main__':
    postjobfree_scraper.run(upload=False)
