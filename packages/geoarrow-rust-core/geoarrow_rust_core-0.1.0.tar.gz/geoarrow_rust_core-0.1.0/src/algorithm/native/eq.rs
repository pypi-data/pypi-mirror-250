use crate::geo_traits::{
    CoordTrait, GeometryCollectionTrait, GeometryTrait, GeometryType, LineStringTrait,
    MultiLineStringTrait, MultiPointTrait, MultiPolygonTrait, PointTrait, PolygonTrait, RectTrait,
};
use arrow_array::OffsetSizeTrait;
use arrow_buffer::OffsetBuffer;
use geo::CoordFloat;

#[inline]
pub fn coord_eq_allow_nan<T: CoordFloat>(
    left: &impl CoordTrait<T = T>,
    right: &impl CoordTrait<T = T>,
) -> bool {
    // Specifically check for NaN because two points defined to be
    // TODO: in the future add an `is_empty` to the PointTrait and then you shouldn't check for
    // NaN manually
    if left.x().is_nan() && right.x().is_nan() && left.y().is_nan() && right.y().is_nan() {
        return true;
    }

    left.x_y() == right.x_y()
}

#[inline]
pub fn coord_eq<T: CoordFloat>(
    left: &impl CoordTrait<T = T>,
    right: &impl CoordTrait<T = T>,
) -> bool {
    left.x_y() == right.x_y()
}

#[inline]
pub fn point_eq<T: CoordFloat>(
    left: &impl PointTrait<T = T>,
    right: &impl PointTrait<T = T>,
    allow_nan_equal: bool,
) -> bool {
    if allow_nan_equal {
        // Specifically check for NaN because two points defined to be
        // TODO: in the future add an `is_empty` to the PointTrait and then you shouldn't check for
        // NaN manually
        if left.x().is_nan() && right.x().is_nan() && left.y().is_nan() && right.y().is_nan() {
            return true;
        }
    }

    left.x_y() == right.x_y()
}

#[inline]
pub fn line_string_eq<T: CoordFloat>(
    left: &impl LineStringTrait<T = T>,
    right: &impl LineStringTrait<T = T>,
) -> bool {
    if left.num_coords() != right.num_coords() {
        return false;
    }

    for coord_idx in 0..left.num_coords() {
        let left_coord = left.coord(coord_idx).unwrap();
        let right_coord = right.coord(coord_idx).unwrap();
        if !coord_eq(&left_coord, &right_coord) {
            return false;
        }
    }

    true
}

#[inline]
pub fn polygon_eq<T: CoordFloat>(
    left: &impl PolygonTrait<T = T>,
    right: &impl PolygonTrait<T = T>,
) -> bool {
    if left.num_interiors() != right.num_interiors() {
        return false;
    }

    match (left.exterior(), right.exterior()) {
        (None, None) => (),
        (Some(_), None) => {
            return false;
        }
        (None, Some(_)) => {
            return false;
        }
        (Some(left), Some(right)) => {
            if !line_string_eq(&left, &right) {
                return false;
            }
        }
    };

    for i in 0..left.num_interiors() {
        if !line_string_eq(&left.interior(i).unwrap(), &right.interior(i).unwrap()) {
            return false;
        }
    }

    true
}

#[inline]
pub fn multi_point_eq<T: CoordFloat>(
    left: &impl MultiPointTrait<T = T>,
    right: &impl MultiPointTrait<T = T>,
) -> bool {
    if left.num_points() != right.num_points() {
        return false;
    }

    for point_idx in 0..left.num_points() {
        let left_point = left.point(point_idx).unwrap();
        let right_point = right.point(point_idx).unwrap();
        if !point_eq(&left_point, &right_point, false) {
            return false;
        }
    }

    true
}

#[inline]
pub fn multi_line_string_eq<T: CoordFloat>(
    left: &impl MultiLineStringTrait<T = T>,
    right: &impl MultiLineStringTrait<T = T>,
) -> bool {
    if left.num_lines() != right.num_lines() {
        return false;
    }

    for line_idx in 0..left.num_lines() {
        if !line_string_eq(
            &left.line(line_idx).unwrap(),
            &right.line(line_idx).unwrap(),
        ) {
            return false;
        }
    }

    true
}

#[inline]
pub fn multi_polygon_eq<T: CoordFloat>(
    left: &impl MultiPolygonTrait<T = T>,
    right: &impl MultiPolygonTrait<T = T>,
) -> bool {
    if left.num_polygons() != right.num_polygons() {
        return false;
    }

    for polygon_idx in 0..left.num_polygons() {
        if !polygon_eq(
            &left.polygon(polygon_idx).unwrap(),
            &right.polygon(polygon_idx).unwrap(),
        ) {
            return false;
        }
    }

    true
}

#[inline]
pub fn rect_eq<T: CoordFloat>(left: &impl RectTrait<T = T>, right: &impl RectTrait<T = T>) -> bool {
    if !coord_eq(&left.lower(), &right.lower()) {
        return false;
    }

    if !coord_eq(&left.upper(), &right.upper()) {
        return false;
    }

    true
}

#[inline]
pub fn geometry_eq<T: CoordFloat>(
    left: &impl GeometryTrait<T = T>,
    right: &impl GeometryTrait<T = T>,
) -> bool {
    match (left.as_type(), right.as_type()) {
        (GeometryType::Point(l), GeometryType::Point(r)) => {
            if !point_eq(l, r, false) {
                return false;
            }
        }
        (GeometryType::LineString(l), GeometryType::LineString(r)) => {
            if !line_string_eq(l, r) {
                return false;
            }
        }
        (GeometryType::Polygon(l), GeometryType::Polygon(r)) => {
            if !polygon_eq(l, r) {
                return false;
            }
        }
        (GeometryType::MultiPoint(l), GeometryType::MultiPoint(r)) => {
            if !multi_point_eq(l, r) {
                return false;
            }
        }
        (GeometryType::MultiLineString(l), GeometryType::MultiLineString(r)) => {
            if !multi_line_string_eq(l, r) {
                return false;
            }
        }
        (GeometryType::MultiPolygon(l), GeometryType::MultiPolygon(r)) => {
            if !multi_polygon_eq(l, r) {
                return false;
            }
        }
        (GeometryType::Rect(l), GeometryType::Rect(r)) => {
            if !rect_eq(l, r) {
                return false;
            }
        }
        (GeometryType::GeometryCollection(l), GeometryType::GeometryCollection(r)) => {
            if !geometry_collection_eq(l, r) {
                return false;
            }
        }
        _ => {
            return false;
        }
    }

    true
}

#[inline]
pub fn geometry_collection_eq<T: CoordFloat>(
    left: &impl GeometryCollectionTrait<T = T>,
    right: &impl GeometryCollectionTrait<T = T>,
) -> bool {
    if left.num_geometries() != right.num_geometries() {
        return false;
    }

    for geometry_idx in 0..left.num_geometries() {
        let left_geom = left.geometry(geometry_idx).unwrap();
        let right_geom = right.geometry(geometry_idx).unwrap();
        if !geometry_eq(&left_geom, &right_geom) {
            return false;
        }
    }

    true
}

pub(crate) fn offset_buffer_eq<O: OffsetSizeTrait>(
    left: &OffsetBuffer<O>,
    right: &OffsetBuffer<O>,
) -> bool {
    if left.len() != right.len() {
        return false;
    }

    for (o1, o2) in left.iter().zip(right.iter()) {
        if o1 != o2 {
            return false;
        }
    }

    true
}
