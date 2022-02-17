#include "bbox_details.h"

#include <dlib/dir_nav.h>
#include <execution>
#include <pybind11/pybind11.h>
#include <regex>

namespace py = pybind11;

using namespace dlib;

using BBoxList = std::vector<bbox_details>;

PYBIND11_MODULE(bboxloader, m)
{
    m.doc() = "load csv files";
    m.attr("__version__") = "1.0.0";
    py::class_<bbox_details>(m, "BBoxDetails")
        .def(py::init<>(), "Construct an ImageInfo object")
        .def(py::init<const std::string&>(), py::arg("csv line"), "Construct an ImageInfo object")
        .def_readwrite("path", &bbox_details::path, "image path")
        .def_readwrite("xmin", &bbox_details::xmin, "xmin bbox coordinate")
        .def_readwrite("ymin", &bbox_details::ymin, "ymin bbox coordinate")
        .def_readwrite("xmax", &bbox_details::xmax, "xmax bbox coordinate")
        .def_readwrite("ymax", &bbox_details::ymax, "ymax bbox coordinate")
        .def_readwrite("conf", &bbox_details::conf, "detection confidence")
        .def_readwrite("label", &bbox_details::label, "class label")
        .def_readwrite("bbox_id", &bbox_details::bbox_id, "bounding box id")
        .def(
            "__eq__",
            [](const bbox_details& a, const bbox_details& b) { return a.bbox_id == b.bbox_id; })
        .def(
            "__repr__",
            [](const bbox_details& item)
            {
                std::ostringstream sout;
                sout << "BBoxDetails(\n";
                sout << " path:    " << item.path << '\n';
                sout << " xmin:    " << item.xmin << '\n';
                sout << " ymin:    " << item.ymin << '\n';
                sout << " xmax:    " << item.xmax << '\n';
                sout << " ymax:    " << item.ymax << '\n';
                sout << " conf:    " << item.conf << '\n';
                sout << " label:   " << item.label << '\n';
                sout << " bbox_id: " << item.bbox_id << '\n';
                sout << ")";
                return sout.str();
            });

    py::class_<BBoxList>(m, "InfosList")
        .def(py::init<>(), "Construct an InfosList object")
        .def("__len__", [](const BBoxList& l) { return l.size(); })
        .def("__iter__", [](BBoxList& l) { return py::make_iterator(l.begin(), l.end()); })
        .def("__getitem__", [](BBoxList& l, size_t index) { return l[index]; })
        .def("append", [](BBoxList& l, const bbox_details& i) { l.push_back(i); })
        .def("clear", &BBoxList::clear)
        .def("save", [](const BBoxList& l, const std::string& path) { serialize(path) << l; })
        .def("load", [](BBoxList& l, const std::string& path) { deserialize(path) >> l; })
        .def(
            "find_bbox_id",
            [](BBoxList& l, const std::string& id)
            {
                const auto p = std::find_if(
                                   std::execution::par_unseq,
                                   l.begin(),
                                   l.end(),
                                   [&id](const auto i) { return i.bbox_id == id; }) -
                               l.begin();
                if (p == l.size())
                    return -1l;
                else
                    return p;
            })
        .def(py::pickle(
            [](const BBoxList& l) { return py::make_tuple(l.size(), std::string("listing.dat")); },
            [](py::tuple t)
            {
                if (t.size() != 2)
                    throw std::runtime_error("Invalid state");
                BBoxList l;
                const size_t size = t[0].cast<size_t>();
                deserialize(t[1].cast<std::string>()) >> l;
                return l;
            }));

    m.def(
        "load_csv_files",
        [](const std::string& path)
        {
            const auto files = dlib::get_files_in_directory_tree(path, dlib::match_ending(".csv"));
            BBoxList listing;
            for (const auto& file : files)
            {
                load_csv_file(file.full_name(), listing, true);
            }
            return listing;
        },
        py::arg("path"));
}
