# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs
from ._inputs import *

__all__ = ['EntityArgs', 'Entity']

@pulumi.input_type
class EntityArgs:
    def __init__(__self__, *,
                 blueprint: pulumi.Input[str],
                 icon: Optional[pulumi.Input[str]] = None,
                 identifier: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input['EntityPropertiesArgs']] = None,
                 relations: Optional[pulumi.Input['EntityRelationsArgs']] = None,
                 run_id: Optional[pulumi.Input[str]] = None,
                 teams: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 title: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Entity resource.
        :param pulumi.Input[str] blueprint: The blueprint identifier the entity relates to
        :param pulumi.Input[str] icon: The icon of the entity
        :param pulumi.Input[str] identifier: The identifier of the entity
        :param pulumi.Input['EntityPropertiesArgs'] properties: The properties of the entity
        :param pulumi.Input['EntityRelationsArgs'] relations: The relations of the entity
        :param pulumi.Input[str] run_id: The runID of the action run that created the entity
        :param pulumi.Input[Sequence[pulumi.Input[str]]] teams: The teams the entity belongs to
        :param pulumi.Input[str] title: The title of the entity
        """
        pulumi.set(__self__, "blueprint", blueprint)
        if icon is not None:
            pulumi.set(__self__, "icon", icon)
        if identifier is not None:
            pulumi.set(__self__, "identifier", identifier)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)
        if relations is not None:
            pulumi.set(__self__, "relations", relations)
        if run_id is not None:
            pulumi.set(__self__, "run_id", run_id)
        if teams is not None:
            pulumi.set(__self__, "teams", teams)
        if title is not None:
            pulumi.set(__self__, "title", title)

    @property
    @pulumi.getter
    def blueprint(self) -> pulumi.Input[str]:
        """
        The blueprint identifier the entity relates to
        """
        return pulumi.get(self, "blueprint")

    @blueprint.setter
    def blueprint(self, value: pulumi.Input[str]):
        pulumi.set(self, "blueprint", value)

    @property
    @pulumi.getter
    def icon(self) -> Optional[pulumi.Input[str]]:
        """
        The icon of the entity
        """
        return pulumi.get(self, "icon")

    @icon.setter
    def icon(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "icon", value)

    @property
    @pulumi.getter
    def identifier(self) -> Optional[pulumi.Input[str]]:
        """
        The identifier of the entity
        """
        return pulumi.get(self, "identifier")

    @identifier.setter
    def identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "identifier", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input['EntityPropertiesArgs']]:
        """
        The properties of the entity
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input['EntityPropertiesArgs']]):
        pulumi.set(self, "properties", value)

    @property
    @pulumi.getter
    def relations(self) -> Optional[pulumi.Input['EntityRelationsArgs']]:
        """
        The relations of the entity
        """
        return pulumi.get(self, "relations")

    @relations.setter
    def relations(self, value: Optional[pulumi.Input['EntityRelationsArgs']]):
        pulumi.set(self, "relations", value)

    @property
    @pulumi.getter(name="runId")
    def run_id(self) -> Optional[pulumi.Input[str]]:
        """
        The runID of the action run that created the entity
        """
        return pulumi.get(self, "run_id")

    @run_id.setter
    def run_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "run_id", value)

    @property
    @pulumi.getter
    def teams(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The teams the entity belongs to
        """
        return pulumi.get(self, "teams")

    @teams.setter
    def teams(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "teams", value)

    @property
    @pulumi.getter
    def title(self) -> Optional[pulumi.Input[str]]:
        """
        The title of the entity
        """
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "title", value)


@pulumi.input_type
class _EntityState:
    def __init__(__self__, *,
                 blueprint: Optional[pulumi.Input[str]] = None,
                 created_at: Optional[pulumi.Input[str]] = None,
                 created_by: Optional[pulumi.Input[str]] = None,
                 icon: Optional[pulumi.Input[str]] = None,
                 identifier: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input['EntityPropertiesArgs']] = None,
                 relations: Optional[pulumi.Input['EntityRelationsArgs']] = None,
                 run_id: Optional[pulumi.Input[str]] = None,
                 teams: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 title: Optional[pulumi.Input[str]] = None,
                 updated_at: Optional[pulumi.Input[str]] = None,
                 updated_by: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Entity resources.
        :param pulumi.Input[str] blueprint: The blueprint identifier the entity relates to
        :param pulumi.Input[str] created_at: The creation date of the entity
        :param pulumi.Input[str] created_by: The creator of the entity
        :param pulumi.Input[str] icon: The icon of the entity
        :param pulumi.Input[str] identifier: The identifier of the entity
        :param pulumi.Input['EntityPropertiesArgs'] properties: The properties of the entity
        :param pulumi.Input['EntityRelationsArgs'] relations: The relations of the entity
        :param pulumi.Input[str] run_id: The runID of the action run that created the entity
        :param pulumi.Input[Sequence[pulumi.Input[str]]] teams: The teams the entity belongs to
        :param pulumi.Input[str] title: The title of the entity
        :param pulumi.Input[str] updated_at: The last update date of the entity
        :param pulumi.Input[str] updated_by: The last updater of the entity
        """
        if blueprint is not None:
            pulumi.set(__self__, "blueprint", blueprint)
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if created_by is not None:
            pulumi.set(__self__, "created_by", created_by)
        if icon is not None:
            pulumi.set(__self__, "icon", icon)
        if identifier is not None:
            pulumi.set(__self__, "identifier", identifier)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)
        if relations is not None:
            pulumi.set(__self__, "relations", relations)
        if run_id is not None:
            pulumi.set(__self__, "run_id", run_id)
        if teams is not None:
            pulumi.set(__self__, "teams", teams)
        if title is not None:
            pulumi.set(__self__, "title", title)
        if updated_at is not None:
            pulumi.set(__self__, "updated_at", updated_at)
        if updated_by is not None:
            pulumi.set(__self__, "updated_by", updated_by)

    @property
    @pulumi.getter
    def blueprint(self) -> Optional[pulumi.Input[str]]:
        """
        The blueprint identifier the entity relates to
        """
        return pulumi.get(self, "blueprint")

    @blueprint.setter
    def blueprint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "blueprint", value)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[pulumi.Input[str]]:
        """
        The creation date of the entity
        """
        return pulumi.get(self, "created_at")

    @created_at.setter
    def created_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_at", value)

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> Optional[pulumi.Input[str]]:
        """
        The creator of the entity
        """
        return pulumi.get(self, "created_by")

    @created_by.setter
    def created_by(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_by", value)

    @property
    @pulumi.getter
    def icon(self) -> Optional[pulumi.Input[str]]:
        """
        The icon of the entity
        """
        return pulumi.get(self, "icon")

    @icon.setter
    def icon(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "icon", value)

    @property
    @pulumi.getter
    def identifier(self) -> Optional[pulumi.Input[str]]:
        """
        The identifier of the entity
        """
        return pulumi.get(self, "identifier")

    @identifier.setter
    def identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "identifier", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input['EntityPropertiesArgs']]:
        """
        The properties of the entity
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input['EntityPropertiesArgs']]):
        pulumi.set(self, "properties", value)

    @property
    @pulumi.getter
    def relations(self) -> Optional[pulumi.Input['EntityRelationsArgs']]:
        """
        The relations of the entity
        """
        return pulumi.get(self, "relations")

    @relations.setter
    def relations(self, value: Optional[pulumi.Input['EntityRelationsArgs']]):
        pulumi.set(self, "relations", value)

    @property
    @pulumi.getter(name="runId")
    def run_id(self) -> Optional[pulumi.Input[str]]:
        """
        The runID of the action run that created the entity
        """
        return pulumi.get(self, "run_id")

    @run_id.setter
    def run_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "run_id", value)

    @property
    @pulumi.getter
    def teams(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The teams the entity belongs to
        """
        return pulumi.get(self, "teams")

    @teams.setter
    def teams(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "teams", value)

    @property
    @pulumi.getter
    def title(self) -> Optional[pulumi.Input[str]]:
        """
        The title of the entity
        """
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "title", value)

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> Optional[pulumi.Input[str]]:
        """
        The last update date of the entity
        """
        return pulumi.get(self, "updated_at")

    @updated_at.setter
    def updated_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "updated_at", value)

    @property
    @pulumi.getter(name="updatedBy")
    def updated_by(self) -> Optional[pulumi.Input[str]]:
        """
        The last updater of the entity
        """
        return pulumi.get(self, "updated_by")

    @updated_by.setter
    def updated_by(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "updated_by", value)


class Entity(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 blueprint: Optional[pulumi.Input[str]] = None,
                 icon: Optional[pulumi.Input[str]] = None,
                 identifier: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['EntityPropertiesArgs']]] = None,
                 relations: Optional[pulumi.Input[pulumi.InputType['EntityRelationsArgs']]] = None,
                 run_id: Optional[pulumi.Input[str]] = None,
                 teams: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 title: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Create a Entity resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] blueprint: The blueprint identifier the entity relates to
        :param pulumi.Input[str] icon: The icon of the entity
        :param pulumi.Input[str] identifier: The identifier of the entity
        :param pulumi.Input[pulumi.InputType['EntityPropertiesArgs']] properties: The properties of the entity
        :param pulumi.Input[pulumi.InputType['EntityRelationsArgs']] relations: The relations of the entity
        :param pulumi.Input[str] run_id: The runID of the action run that created the entity
        :param pulumi.Input[Sequence[pulumi.Input[str]]] teams: The teams the entity belongs to
        :param pulumi.Input[str] title: The title of the entity
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EntityArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a Entity resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param EntityArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EntityArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 blueprint: Optional[pulumi.Input[str]] = None,
                 icon: Optional[pulumi.Input[str]] = None,
                 identifier: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['EntityPropertiesArgs']]] = None,
                 relations: Optional[pulumi.Input[pulumi.InputType['EntityRelationsArgs']]] = None,
                 run_id: Optional[pulumi.Input[str]] = None,
                 teams: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 title: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EntityArgs.__new__(EntityArgs)

            if blueprint is None and not opts.urn:
                raise TypeError("Missing required property 'blueprint'")
            __props__.__dict__["blueprint"] = blueprint
            __props__.__dict__["icon"] = icon
            __props__.__dict__["identifier"] = identifier
            __props__.__dict__["properties"] = properties
            __props__.__dict__["relations"] = relations
            __props__.__dict__["run_id"] = run_id
            __props__.__dict__["teams"] = teams
            __props__.__dict__["title"] = title
            __props__.__dict__["created_at"] = None
            __props__.__dict__["created_by"] = None
            __props__.__dict__["updated_at"] = None
            __props__.__dict__["updated_by"] = None
        super(Entity, __self__).__init__(
            'port:index/entity:Entity',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            blueprint: Optional[pulumi.Input[str]] = None,
            created_at: Optional[pulumi.Input[str]] = None,
            created_by: Optional[pulumi.Input[str]] = None,
            icon: Optional[pulumi.Input[str]] = None,
            identifier: Optional[pulumi.Input[str]] = None,
            properties: Optional[pulumi.Input[pulumi.InputType['EntityPropertiesArgs']]] = None,
            relations: Optional[pulumi.Input[pulumi.InputType['EntityRelationsArgs']]] = None,
            run_id: Optional[pulumi.Input[str]] = None,
            teams: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            title: Optional[pulumi.Input[str]] = None,
            updated_at: Optional[pulumi.Input[str]] = None,
            updated_by: Optional[pulumi.Input[str]] = None) -> 'Entity':
        """
        Get an existing Entity resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] blueprint: The blueprint identifier the entity relates to
        :param pulumi.Input[str] created_at: The creation date of the entity
        :param pulumi.Input[str] created_by: The creator of the entity
        :param pulumi.Input[str] icon: The icon of the entity
        :param pulumi.Input[str] identifier: The identifier of the entity
        :param pulumi.Input[pulumi.InputType['EntityPropertiesArgs']] properties: The properties of the entity
        :param pulumi.Input[pulumi.InputType['EntityRelationsArgs']] relations: The relations of the entity
        :param pulumi.Input[str] run_id: The runID of the action run that created the entity
        :param pulumi.Input[Sequence[pulumi.Input[str]]] teams: The teams the entity belongs to
        :param pulumi.Input[str] title: The title of the entity
        :param pulumi.Input[str] updated_at: The last update date of the entity
        :param pulumi.Input[str] updated_by: The last updater of the entity
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _EntityState.__new__(_EntityState)

        __props__.__dict__["blueprint"] = blueprint
        __props__.__dict__["created_at"] = created_at
        __props__.__dict__["created_by"] = created_by
        __props__.__dict__["icon"] = icon
        __props__.__dict__["identifier"] = identifier
        __props__.__dict__["properties"] = properties
        __props__.__dict__["relations"] = relations
        __props__.__dict__["run_id"] = run_id
        __props__.__dict__["teams"] = teams
        __props__.__dict__["title"] = title
        __props__.__dict__["updated_at"] = updated_at
        __props__.__dict__["updated_by"] = updated_by
        return Entity(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def blueprint(self) -> pulumi.Output[str]:
        """
        The blueprint identifier the entity relates to
        """
        return pulumi.get(self, "blueprint")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> pulumi.Output[str]:
        """
        The creation date of the entity
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> pulumi.Output[str]:
        """
        The creator of the entity
        """
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter
    def icon(self) -> pulumi.Output[Optional[str]]:
        """
        The icon of the entity
        """
        return pulumi.get(self, "icon")

    @property
    @pulumi.getter
    def identifier(self) -> pulumi.Output[str]:
        """
        The identifier of the entity
        """
        return pulumi.get(self, "identifier")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output[Optional['outputs.EntityProperties']]:
        """
        The properties of the entity
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def relations(self) -> pulumi.Output[Optional['outputs.EntityRelations']]:
        """
        The relations of the entity
        """
        return pulumi.get(self, "relations")

    @property
    @pulumi.getter(name="runId")
    def run_id(self) -> pulumi.Output[Optional[str]]:
        """
        The runID of the action run that created the entity
        """
        return pulumi.get(self, "run_id")

    @property
    @pulumi.getter
    def teams(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The teams the entity belongs to
        """
        return pulumi.get(self, "teams")

    @property
    @pulumi.getter
    def title(self) -> pulumi.Output[Optional[str]]:
        """
        The title of the entity
        """
        return pulumi.get(self, "title")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> pulumi.Output[str]:
        """
        The last update date of the entity
        """
        return pulumi.get(self, "updated_at")

    @property
    @pulumi.getter(name="updatedBy")
    def updated_by(self) -> pulumi.Output[str]:
        """
        The last updater of the entity
        """
        return pulumi.get(self, "updated_by")

