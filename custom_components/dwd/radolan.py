# -*- coding: utf-8 -*-
"""
Created on Tue May  7 22:58:05 2024

@author: Bobby
"""

import bz2

import wradlib as wrl

import httpx
import numpy as np

from datetime import datetime, timedelta, timezone

from homeassistant.helpers.httpx_client import get_async_client


from .const import DWD_RADOLAN_URL


class Radolan:
    """DWD Radolan class."""

    def __init__(
            self,
            radolan_type: str,
            latitude: float,
            longitude: float,
            async_client: httpx.AsyncClient
    ) -> None:
        """Initialize instance."""
        self._radolan_type = radolan_type
        self._async_client = async_client
        self._lat = latitude
        self._lon = longitude
        self._last_etag = None
        
        
        self._last_grid_update = datetime.now(timezone.utc)
        self.curr_value = None
        
    @property
    def key(self) -> None:
        """Return the key."""
        return f"radolan_{self._radolan_type}"
        
    async def update(self):
        """Update Radolan data."""
        url = self._get_url()
        headers = {}
        if self.last_etag is not None:
            headers["If-None-Match"] = self._last_etag


        resp = await self._async_client.get(url, headers=headers)
        
        if resp.status_code == 304:
            return self.curr_value
        
        if resp.status_code != httpx.codes.OK:
            resp.raise_for_status()
        
        self.curr_value = self._parse(resp)
        
        return self.curr_value
    
    def _get_url(self) -> str:
        """Return the url."""
        fname = f"raa01-{self._radolan_type}_10000-latest-dwd---bin.bz2"
        return f"{DWD_RADOLAN_URL}/{self._radolan_type}/{fname}"

    def _parse(self, response):
        """Parse the response."""
        data = bz2.BZ2File(response).read()
        ds = wrl.io.open_radolan_dataset(data)
        radolan_grid_ll = self._get_radolan_grid(ds)
        ds = ds.assign_coords(
            {"lon": (["y", "x"], radolan_grid_ll[..., 0]),
             "lat": (["y", "x"], radolan_grid_ll[..., 1])}
        )

        abslat = np.abs(ds.lat-self._lat)
        abslon = np.abs(ds.lon-self._lon)
        c = np.maximum(abslon, abslat)

        # Attention: y/lat is first dim, get
        ([yidx], [xidx]) = np.where(c == np.min(c))

        # Select index location at the x/y dimension
        # use isel as we select with index
        point_ds = ds.isel(x=xidx, y=yidx)

        return point_ds.RW.values

    def _get_radolan_grid(self, ds):
        """Return the radolan lat, lon grid."""
        grid_age = datetime.now(timezone.utc) - self._last_grid_update
        to_refresh = grid_age > timedelta(hours=24)
        if to_refresh or self._radolan_grid_ll is None:
            self._radolan_grid_ll = wrl.georef.get_radolan_grid(
                nrows=ds.dims["y"],
                ncols=ds.dims["x"],
                wgs84=True,
                mode="radolan",
                # proj=proj_stereo
            )

        return self._radolan_grid_ll
    