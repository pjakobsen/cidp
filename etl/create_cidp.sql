--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: browser; Type: TABLE; Schema: public; Owner: peder; Tablespace: 
--

CREATE TABLE browser (
    id integer NOT NULL,
    project_number character varying(10),
    date_modified date,
    title text,
    description text,
    status text,
    start_date date,
    end_date date,
    country text,
    executing_agency_partner text,
    cida_sector_of_focus text,
    dac_sector text,
    maximum_cida_contribution numeric,
    expected_results text,
    progress_and_results_achieved text
);


ALTER TABLE public.browser OWNER TO peder;

--
-- Name: browser_id_seq; Type: SEQUENCE; Schema: public; Owner: peder
--

CREATE SEQUENCE browser_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.browser_id_seq OWNER TO peder;

--
-- Name: browser_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: peder
--

ALTER SEQUENCE browser_id_seq OWNED BY browser.id;


--
-- Name: hpds; Type: TABLE; Schema: public; Owner: peder; Tablespace: 
--

CREATE TABLE hpds (
    id integer NOT NULL,
    browser_id integer,
    fiscal_year date,
    project_number text,
    status text,
    maximum_cida_contribution double precision,
    branch_id text,
    branch_name text,
    division_id text,
    division_name text,
    section_id text,
    section_name text,
    regional_program text,
    fund_centre_id text,
    fund_centre_name text,
    untied_amount double precision,
    fstc_percent text,
    irtc_percent text,
    cfli text,
    cida_business_delivery_model character varying(200),
    bilateral_aid text,
    pba_type text,
    environmental_sustainability text,
    climate_change_adaptation text,
    climate_change_mitigation text,
    desertification text,
    participatory_development_and_good_governance text,
    trade_development text,
    biodiversity text,
    urban_issues text,
    children_issues text,
    youth_issues text,
    indigenous_issues text,
    disability_issues text,
    ict_as_a_tool_for_development text,
    knowledge_for_development text,
    gender_equality text,
    organisation_id text,
    organisation_name text,
    organisation_type text,
    organisation_class text,
    organisation_sub_class text,
    continent_id text,
    continent_name text,
    project_browser_country_id text,
    country_region_id text,
    country_region_name text,
    country_region_percent text,
    sector_id text,
    sector_name text,
    sector_percent text,
    amount_spent numeric
);


ALTER TABLE public.hpds OWNER TO peder;

--
-- Name: hpds_id_seq; Type: SEQUENCE; Schema: public; Owner: peder
--

CREATE SEQUENCE hpds_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.hpds_id_seq OWNER TO peder;

--
-- Name: hpds_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: peder
--

ALTER SEQUENCE hpds_id_seq OWNED BY hpds.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: peder
--

ALTER TABLE ONLY browser ALTER COLUMN id SET DEFAULT nextval('browser_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: peder
--

ALTER TABLE ONLY hpds ALTER COLUMN id SET DEFAULT nextval('hpds_id_seq'::regclass);


--
-- Name: browser_pkey; Type: CONSTRAINT; Schema: public; Owner: peder; Tablespace: 
--

ALTER TABLE ONLY browser
    ADD CONSTRAINT browser_pkey PRIMARY KEY (id);


--
-- Name: hpds_pkey; Type: CONSTRAINT; Schema: public; Owner: peder; Tablespace: 
--

ALTER TABLE ONLY hpds
    ADD CONSTRAINT hpds_pkey PRIMARY KEY (id);


--
-- Name: hpds_browser_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: peder
--

ALTER TABLE ONLY hpds
    ADD CONSTRAINT hpds_browser_id_fkey FOREIGN KEY (browser_id) REFERENCES browser(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: peder
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM peder;
GRANT ALL ON SCHEMA public TO peder;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

