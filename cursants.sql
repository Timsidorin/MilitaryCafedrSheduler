/*
 Navicat Premium Data Transfer

 Source Server         : КонструкторТренингов
 Source Server Type    : PostgreSQL
 Source Server Version : 160003 (160003)
 Source Host           : localhost:5432
 Source Catalog        : postgres
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 160003 (160003)
 File Encoding         : 65001

 Date: 22/09/2025 21:28:43
*/


-- ----------------------------
-- Table structure for cursants
-- ----------------------------
DROP TABLE IF EXISTS "public"."cursants";
CREATE TABLE "public"."cursants" (
  "id" int4 NOT NULL DEFAULT nextval('cursants_id_seq'::regclass),
  "name" varchar(50) COLLATE "pg_catalog"."default",
  "currentstatus" char(1) COLLATE "pg_catalog"."default" DEFAULT '0'::bpchar,
  "telegram_name" varchar(100) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of cursants
-- ----------------------------
INSERT INTO "public"."cursants" VALUES (4, 'Ермолаев', '0', 'squad468');
INSERT INTO "public"."cursants" VALUES (3, 'Дугаёв', '0', 'Дугаёв');
INSERT INTO "public"."cursants" VALUES (2, 'Горбатов', '0', 'kompotzz');
INSERT INTO "public"."cursants" VALUES (1, 'Блинов', '0', 'oladish_04');
INSERT INTO "public"."cursants" VALUES (11, 'Фаррахов', '0', 'k37363627');
INSERT INTO "public"."cursants" VALUES (12, 'Черненко', '0', 'PrintHell0W0rld');
INSERT INTO "public"."cursants" VALUES (13, 'Чубаров', '0', 'qzuezq');
INSERT INTO "public"."cursants" VALUES (14, 'Яровенко', '0', 'i4ib0');
INSERT INTO "public"."cursants" VALUES (8, 'Парамонов', '0', 'Babuin_God');
INSERT INTO "public"."cursants" VALUES (10, 'Репин', '0', 'Momongasan');
INSERT INTO "public"."cursants" VALUES (6, 'Каргин', '0', 'ymhkun');
INSERT INTO "public"."cursants" VALUES (9, 'Пастухов', '0', 'Пастухов');
INSERT INTO "public"."cursants" VALUES (7, 'Кононов', '0', 'Dmitry_pajiloy');

-- ----------------------------
-- Indexes structure for table cursants
-- ----------------------------
CREATE INDEX "idx_cursants_id_status" ON "public"."cursants" USING btree (
  "id" "pg_catalog"."int4_ops" ASC NULLS LAST,
  "currentstatus" COLLATE "pg_catalog"."default" "pg_catalog"."bpchar_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table cursants
-- ----------------------------
ALTER TABLE "public"."cursants" ADD CONSTRAINT "cursants_pkey" PRIMARY KEY ("id");
