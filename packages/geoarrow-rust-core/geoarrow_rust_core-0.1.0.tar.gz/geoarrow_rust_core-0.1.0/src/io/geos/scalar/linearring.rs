use crate::error::{GeoArrowError, Result};
use crate::geo_traits::LineStringTrait;
use crate::io::geos::scalar::coord::GEOSConstCoord;
use geos::{Geom, GeometryTypes};
use std::iter::Cloned;
use std::slice::Iter;

pub struct GEOSConstLinearRing<'a, 'b>(pub(crate) geos::ConstGeometry<'a, 'b>);

impl<'a, 'b> GEOSConstLinearRing<'a, 'b> {
    pub fn new_unchecked(geom: geos::ConstGeometry<'a, 'b>) -> Self {
        Self(geom)
    }

    #[allow(dead_code)]
    pub fn try_new(geom: geos::ConstGeometry<'a, 'b>) -> Result<Self> {
        if matches!(geom.geometry_type(), GeometryTypes::LinearRing) {
            Ok(Self(geom))
        } else {
            Err(GeoArrowError::General(
                "Geometry type must be linear ring".to_string(),
            ))
        }
    }

    pub fn num_coords(&self) -> usize {
        self.0.get_num_coordinates().unwrap()
    }
}

impl<'a, 'b> LineStringTrait for GEOSConstLinearRing<'a, 'b> {
    type T = f64;
    type ItemType<'c> = GEOSConstCoord<'a> where Self: 'c;
    type Iter<'c> = Cloned<Iter<'c, Self::ItemType<'c>>> where Self: 'c;

    fn num_coords(&self) -> usize {
        self.0.get_num_coordinates().unwrap()
    }

    fn coord(&self, i: usize) -> Option<Self::ItemType<'_>> {
        if i > (self.num_coords()) {
            return None;
        }

        let seq = self.0.get_coord_seq().unwrap();
        Some(GEOSConstCoord {
            coords: seq,
            geom_index: i,
        })
    }

    fn coords(&self) -> Self::Iter<'_> {
        todo!()
    }
}

// This is a big HACK to try and get the PolygonTrait to successfully implement on
// GEOSPolygon. We never use this because we never use the trait iterators.
impl<'a, 'b> Clone for GEOSConstLinearRing<'a, 'b> {
    fn clone(&self) -> Self {
        todo!()
    }

    fn clone_from(&mut self, _source: &Self) {
        todo!()
    }
}
