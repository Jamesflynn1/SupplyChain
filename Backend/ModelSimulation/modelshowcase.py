import Application
import datetime

start_date = datetime.datetime(2001, 1, 1)

epi_application = Application.ModelBackend(start_date=start_date, model_folder="../ModelFiles/RegionalEpi/")
out = epi_application.simulate(time_limit=365)

out.plotAllClassesOverTime(location_index=0)