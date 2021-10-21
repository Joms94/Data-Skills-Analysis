'''
Run all scrapers, upload all material, then calculate insights.
'''
from scraper_instances import postjobfree_scraper, jobserve_scraper
from insights import update_all_insights
from database_interaction import drop_duplicates_from_database
from extract_and_transform import perform_all_transformations


def perform_all_operations( 
                            run_scrapers:bool=True,
                            drop_duplicates:bool=True, 
                            perform_transformations:bool=True, 
                            update_insights:bool=True, 
                            **scrapers):
    if run_scrapers == True:
        for scraper in scrapers:
            try:
                scraper.values()
            finally:
                continue
    if drop_duplicates == True:
        try:
            drop_duplicates_from_database()
        finally:
            pass
    if perform_transformations == True:
        try:
            perform_all_transformations()
        finally:
            pass
    if update_insights == True:
        try:
            update_all_insights()
        finally:
            pass
    print('All operations completed.')


if __name__ == '__main__':
    perform_all_operations(
                            run_scrapers=True, 
                            drop_duplicates=True,
                            update_insights=True,
                            perform_transformations=True,
                            scrapers1=postjobfree_scraper.run(upload=True), 
                            scrapers2=jobserve_scraper.run(upload=True)
                            )
