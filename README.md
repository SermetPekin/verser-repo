[![Python package](https://github.com/SermetPekin/verser-repo/actions/workflows/python-package.yml/badge.svg)](https://github.com/SermetPekin/verser-repo/actions/workflows/python-package.yml)
[![Downloads](https://pepy.tech/badge/verser/week)](https://pepy.tech/project/verser)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-310/)

# verser

    from verser import  * 


### next_version_pypi 
> makes a request to PYPI server to get information about your package
> then increments it depending on your choices

    def next_version_pypi(package_name: str, increment_choice: bool = True, part: str = "patch"):
        return increment_version_pypi(package_name=package_name, increment_choice=increment_choice, part=part)


### next_version_local 
> If you just want to increment your package version with local version file 
> this function will try to get information about your package from the local path 
> of version file (default : '__version__.py') then increments it depending on your choices
> 

    new_version =  next_version_local( 
        package_name = 'requests' , 
        increment_choice = True,  => if selected False it will not increment current version 
        part = "minor"              => it will increment minoır part of your package version 
        write = True ,              => since write is True it will rewrite current version to the version file 
    )
    print(new_version)
        # defaults 
    #   --------next_version_pypi-------
    #   increment_choice = True ,   => if selected False it will not increment current version 
    #   part='patch'                 => it will ignore this parameter
    #   write = True ,              => since write is True it will rewrite current version to the version file 


### next_version 
    project = Project('verser', version_file_path=Path('verser/__version__.py'))
    
    nv = next_version(project, write=True)
    # defaults 
    #   --------next_version-------
    #   pypi = True , 
    #   write = True ,  
    #   part='patch'

or with a package name
### next_version_with_package_name 
    ## next_version_with_package_name
    nv = next_version_with_package_name(package_name="my_cool_package")
    print(nv)

or with a Package class instance

    project = Project(package_name="my_cool_package",
                                         version_file_path=Path("__version__.py")
                                         )

    new_version = next_version( project=project, part='patch', pypi=True , write = True   )

if your package is not on PYPI server yet you may use the following

> > this will try to read your __version__.py file locally

    project =  Project('my_cool_package' , Path('my_cool_package/my_cool_package')
    next_version( project = project, part='patch', pypi = False  , write = True   )

> > in order to increment current version to a pre-release function you may use it as following

    project =  Project('my_cool_package' , Path('my_cool_package/my_cool_package')
    next_version( project = project, part='pre', pypi = False  , write = True   )

or for PYPI package pypi parameter should be given True

### next_version 
    next_version( project = project, part='pre', pypi = True , write = True  )

> in order to increase just build number this function can be used

    next_version( project = project, part='build', pypi = False , write = True  )

or

    new_version = next_version( project = project, part='build', pypi = False    )

or

    new_version =  next_version_local( 
        package_name = 'my_cool_package' , 
        increment_choice = True, 
        part = "minor" 
    )

## some examples

    new_version = increment_version_pypi('rich')
    print(new_version)
    # results :  12.6.1 
    
    new_version = increment_version_pypi('rich' , part = 'minor')
    print(new_version)
    # results :  12.7.0 

Below example will not only get the next version but also create __version__py. file in the root of the project
this may be used in setup.py file of the project

### next_version 
    project = Project('verser', version_file_path=Path('verser/__version__.py'))
    
    nv = next_version(project, write=True)
    # defaults 
    #   --------next_version-------
    #   pypi = True , 
    #   write = True ,  
    #   part='patch'
    
### next_version_pypi 
    new_version =  next_version_pypi( 
        package_name = 'rich' , 
        increment_choice = True, 
        part = "minor" 
        write = True ,  
    )
    print(new_version)
        # defaults 
    #   --------next_version_pypi-------
    #   increment_choice = True ,   => if selected False it will not increment current version 
    #   part='patch'                 => it will ignore this parameter
    #   write = True ,              => since write is True it will rewrite current version to the version file 

### next_version_local 
    new_version =  next_version_local( 
        package_name = 'requests' , 
        increment_choice = True,  => if selected False it will not increment current version 
        part = "minor"              => it will increment minoır part of your package version 
        write = True ,              => since write is True it will rewrite current version to the version file 
    )
    print(new_version)
        # defaults 
    #   --------next_version_pypi-------
    #   increment_choice = True ,   => if selected False it will not increment current version 
    #   part='patch'                 => it will ignore this parameter
    #   write = True ,              => since write is True it will rewrite current version to the version file 
