#ifndef bbox_details_h_INCLUDED
#define bbox_details_h_INCLUDED

#include <dlib/data_io.h>
#include <dlib/md5.h>
#include <dlib/serialize.h>
#include <regex>

const inline std::map<std::string, std::string> mapping{
    {"SHOES", "shoe"},
    {"JEWELRIES", "jewelry"},
    {"HATS", "hat"},
    {"OUTWEARS", "outer"},
    {"PANTS", "pants"},
    {"SKIRTS", "skirt"},
    {"SWIMWEARS", "swimwear"},
    {"TOPS", "top"},
    {"WHOLEBODIES", "wholebody"},
    {"BAGS", "bag"},
    {"BELTS", "belt"},
    {"GLASSES", "glasses"},
    {"GLOVES", "glove"},
    {"HAIR_ACCESSORIES", "hairpin"},
    {"KEY_RING", "keyring"},
    {"SCARF/MUFFLER", "scarf"},
    {"SOCKS", "sock"},
    {"TIE", "tie"},
    {"WATCHES", "watch"},
};

template <typename T> auto parse_token(std::istringstream& iss, char sep = ',') -> T
{
    T item;
    std::string token;
    std::getline(iss, token, sep);
    std::istringstream sin(token);
    sin >> item;
    return item;
}

template <typename T>
auto load_csv_file(const std::string& csv_path, std::vector<T>& items, bool has_header = true)
{
    std::ifstream data(csv_path);
    std::string line;
    if (has_header)
        std::getline(data, line);
    const std::string prefix = std::regex_replace(
        csv_path.substr(0, csv_path.rfind('.')),
        std::regex("labels"),
        "images");
    while (std::getline(data, line))
    {
        items.emplace_back(line);
        items.back().path = prefix + items.back().path;
    }
}

struct bbox_details
{
    bbox_details() = default;
    bbox_details(const std::string& csv_line)
    {
        std::istringstream sin(csv_line);
        parse_token<std::string>(sin);  // ImageID
        parse_token<std::string>(sin);  // CompanyID
        path = parse_token<std::string>(sin);
        path = path.substr(path.rfind('/'));
        width = parse_token<int>(sin);
        height = parse_token<int>(sin);
        xmin = parse_token<int>(sin);
        ymin = parse_token<int>(sin);
        xmax = parse_token<int>(sin);
        ymax = parse_token<int>(sin);
        parse_token<int>(sin);  // DetectionID
        label = mapping.at(parse_token<std::string>(sin));
        conf = parse_token<float>(sin);
        id = compute_id();
    }
    std::string path;
    int width;
    int height;
    int xmin;
    int ymin;
    int xmax;
    int ymax;
    float conf;
    std::string label;
    std::string id;

    std::string compute_id() const
    {
        std::ostringstream sout;
        sout << path << width << height << xmin << ymin << xmax << ymax << label;
        return dlib::md5(sout.str());
    }

    friend bool operator<(const bbox_details& a, const bbox_details& b)
    {
        return a.id < b.id;
    }
};

inline auto serialize(const bbox_details& item, std::ostream& out) -> void
{
    dlib::serialize(item.path, out);
    dlib::serialize(item.width, out);
    dlib::serialize(item.height, out);
    dlib::serialize(item.xmin, out);
    dlib::serialize(item.ymin, out);
    dlib::serialize(item.xmax, out);
    dlib::serialize(item.ymax, out);
    dlib::serialize(item.conf, out);
    dlib::serialize(item.label, out);
    dlib::serialize(item.id, out);
}

inline auto deserialize(bbox_details& item, std::istream& in) -> void
{
    dlib::deserialize(item.path, in);
    dlib::deserialize(item.width, in);
    dlib::deserialize(item.height, in);
    dlib::deserialize(item.xmin, in);
    dlib::deserialize(item.ymin, in);
    dlib::deserialize(item.xmax, in);
    dlib::deserialize(item.ymax, in);
    dlib::deserialize(item.conf, in);
    dlib::deserialize(item.label, in);
    dlib::deserialize(item.id, in);
}

#endif  // bbox_details_h_INCLUDED
