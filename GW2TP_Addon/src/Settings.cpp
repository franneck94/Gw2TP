#include <filesystem>
#include <fstream>

#include "Settings.h"
#include "Shared.h"

const char *IS_VISIBLE = "IsVisible";

namespace Settings
{
    std::mutex Mutex;
    json Settings = json::object();

    void Load(std::filesystem::path aPath)
    {
        if (!std::filesystem::exists(aPath))
        {
            return;
        }

        Settings::Mutex.lock();
        {
            try
            {
                std::ifstream file(aPath);
                Settings = json::parse(file);
                file.close();
            }
            catch (json::parse_error &ex)
            {
                APIDefs->Log(ELogLevel_WARNING, "GW2TP", "Settings.json could not be parsed.");
                APIDefs->Log(ELogLevel_WARNING, "GW2TP", ex.what());
            }
        }
        Settings::Mutex.unlock();

        /* Widget */
        if (!Settings[IS_VISIBLE].is_null())
        {
            Settings[IS_VISIBLE].get_to<bool>(IsVisible);
        }
    }

    void Save(std::filesystem::path aPath)
    {
        Settings::Mutex.lock();
        {
            std::ofstream file(aPath);
            file << Settings.dump(1, '\t') << std::endl;
            file.close();
        }
        Settings::Mutex.unlock();
    }

    /* Global */

    /* Widget */
    bool IsVisible = true;
}
